-- Acid Battle leaderboard/login migration for an existing project that already has:
--   public.acid_players, public.acid_games, public.acid_moves
-- Safe to run more than once.

create extension if not exists pgcrypto with schema extensions;
alter extension pgcrypto set schema extensions;

-- Short-lived browser sessions mean the 4-digit PIN does not have to be sent
-- with every recorded move. Only a SHA-256 hash of the random session token is stored.
create table if not exists public.acid_sessions (
    id uuid primary key default gen_random_uuid(),
    player_id uuid not null references public.acid_players(id) on delete cascade,
    token_hash text not null unique,
    created_at timestamptz not null default now(),
    last_seen_at timestamptz not null default now(),
    expires_at timestamptz not null default (now() + interval '30 days')
);

alter table public.acid_sessions enable row level security;

-- A move number makes move recording idempotent if a phone/browser retries a request.
alter table public.acid_moves add column if not exists move_number integer;
create unique index if not exists acid_moves_game_move_unique
    on public.acid_moves(game_id, move_number)
    where move_number is not null;

create index if not exists acid_sessions_token_idx on public.acid_sessions(token_hash);
create index if not exists acid_sessions_player_idx on public.acid_sessions(player_id);
create index if not exists acid_games_status_idx on public.acid_games(player_id, status);

-- Browser clients must never read/write the underlying tables directly.
revoke all on table public.acid_players from anon, authenticated;
revoke all on table public.acid_games from anon, authenticated;
revoke all on table public.acid_moves from anon, authenticated;
revoke all on table public.acid_sessions from anon, authenticated;

-- Utility: reject names that are unsuitable for a public class leaderboard.
create or replace function public.acid_nickname_allowed(p_nickname text)
returns boolean
language plpgsql
immutable
security definer
set search_path = ''
as $$
declare
    v_name text := btrim(coalesce(p_nickname, ''));
    v_norm text;
begin
    if char_length(v_name) < 3 or char_length(v_name) > 20 then
        return false;
    end if;
    if v_name !~ '^[A-Za-z0-9 _-]+$' then
        return false;
    end if;

    -- Normalize spacing/punctuation plus common numeric substitutions.
    v_norm := lower(regexp_replace(v_name, '[^A-Za-z0-9]', '', 'g'));
    v_norm := translate(v_norm, '013457', 'oieast');

    if v_norm ~ '(fuck|shit|cunt|nigg|fagg|bitch|whore|slut|penis|vagina|pussy|cock)' then
        return false;
    end if;

    if v_norm in ('admin','administrator','professor','instructor','teacher','moderator') then
        return false;
    end if;

    return true;
end;
$$;

create or replace function public.acid_create_player(
    p_course_code text,
    p_nickname text,
    p_pin text
)
returns jsonb
language plpgsql
security definer
set search_path = ''
as $$
declare
    v_player uuid;
    v_token text;
    v_nickname text := btrim(coalesce(p_nickname, ''));
begin
    if coalesce(p_course_code, '') = '' then
        return jsonb_build_object('ok', false, 'error', 'course_not_configured');
    end if;
    if not public.acid_nickname_allowed(v_nickname) then
        return jsonb_build_object('ok', false, 'error', 'nickname_not_allowed');
    end if;
    if coalesce(p_pin, '') !~ '^[0-9]{4}$' then
        return jsonb_build_object('ok', false, 'error', 'pin_invalid');
    end if;

    begin
        insert into public.acid_players(course_code, nickname, pin_hash)
        values (
            p_course_code,
            v_nickname,
            extensions.crypt(p_pin, extensions.gen_salt('bf', 10))
        )
        returning id into v_player;
    exception when unique_violation then
        return jsonb_build_object('ok', false, 'error', 'nickname_taken');
    end;

    v_token := encode(extensions.gen_random_bytes(32), 'hex');
    insert into public.acid_sessions(player_id, token_hash)
    values (v_player, encode(extensions.digest(v_token, 'sha256'), 'hex'));

    return jsonb_build_object(
        'ok', true,
        'player_id', v_player,
        'nickname', v_nickname,
        'session_token', v_token,
        'wins', 0,
        'moves', 0,
        'optimal_moves', 0,
        'optimal_pct', null
    );
end;
$$;

create or replace function public.acid_login_player(
    p_course_code text,
    p_nickname text,
    p_pin text
)
returns jsonb
language plpgsql
security definer
set search_path = ''
as $$
declare
    v_player public.acid_players%rowtype;
    v_token text;
    v_wins bigint;
    v_moves bigint;
    v_optimal bigint;
begin
    select * into v_player
    from public.acid_players
    where course_code = p_course_code and nickname = btrim(coalesce(p_nickname, ''))
    limit 1;

    if v_player.id is null or extensions.crypt(coalesce(p_pin, ''), v_player.pin_hash) <> v_player.pin_hash then
        return jsonb_build_object('ok', false, 'error', 'invalid_login');
    end if;

    update public.acid_players set last_seen_at = now() where id = v_player.id;
    delete from public.acid_sessions where expires_at < now();

    v_token := encode(extensions.gen_random_bytes(32), 'hex');
    insert into public.acid_sessions(player_id, token_hash)
    values (v_player.id, encode(extensions.digest(v_token, 'sha256'), 'hex'));

    select count(*) filter (where status = 'completed' and won is true)
      into v_wins
      from public.acid_games where player_id = v_player.id;

    select count(*), count(*) filter (where optimal is true)
      into v_moves, v_optimal
      from public.acid_moves where player_id = v_player.id;

    return jsonb_build_object(
        'ok', true,
        'player_id', v_player.id,
        'nickname', v_player.nickname::text,
        'session_token', v_token,
        'wins', coalesce(v_wins,0),
        'moves', coalesce(v_moves,0),
        'optimal_moves', coalesce(v_optimal,0),
        'optimal_pct', case when coalesce(v_moves,0) > 0 then round(100.0 * v_optimal / v_moves, 1) else null end
    );
end;
$$;

create or replace function public.acid_my_stats(
    p_course_code text,
    p_session_token text
)
returns jsonb
language plpgsql
security definer
set search_path = ''
as $$
declare
    v_player uuid;
    v_nickname text;
    v_wins bigint;
    v_moves bigint;
    v_optimal bigint;
begin
    select p.id, p.nickname::text into v_player, v_nickname
    from public.acid_sessions s
    join public.acid_players p on p.id = s.player_id
    where s.token_hash = encode(extensions.digest(coalesce(p_session_token,''), 'sha256'), 'hex')
      and s.expires_at > now()
      and p.course_code = p_course_code
    limit 1;

    if v_player is null then
        return jsonb_build_object('ok', false, 'error', 'session_expired');
    end if;

    update public.acid_sessions
       set last_seen_at = now()
     where token_hash = encode(extensions.digest(p_session_token, 'sha256'), 'hex');

    select count(*) filter (where status = 'completed' and won is true)
      into v_wins from public.acid_games where player_id = v_player;
    select count(*), count(*) filter (where optimal is true)
      into v_moves, v_optimal from public.acid_moves where player_id = v_player;

    return jsonb_build_object(
        'ok', true,
        'nickname', v_nickname,
        'wins', coalesce(v_wins,0),
        'moves', coalesce(v_moves,0),
        'optimal_moves', coalesce(v_optimal,0),
        'optimal_pct', case when coalesce(v_moves,0) > 0 then round(100.0 * v_optimal / v_moves, 1) else null end
    );
end;
$$;

create or replace function public.acid_start_game(
    p_course_code text,
    p_session_token text,
    p_solvent text,
    p_deck_size text
)
returns jsonb
language plpgsql
security definer
set search_path = ''
as $$
declare
    v_player uuid;
    v_game uuid;
begin
    select p.id into v_player
    from public.acid_sessions s
    join public.acid_players p on p.id = s.player_id
    where s.token_hash = encode(extensions.digest(coalesce(p_session_token,''), 'sha256'), 'hex')
      and s.expires_at > now()
      and p.course_code = p_course_code
    limit 1;

    if v_player is null then
        return jsonb_build_object('ok', false, 'error', 'session_expired');
    end if;
    if p_solvent not in ('water','dmso') or p_deck_size not in ('25','50','all') then
        return jsonb_build_object('ok', false, 'error', 'game_settings_invalid');
    end if;

    -- Starting a new game cleanly abandons any previous unfinished game.
    update public.acid_games
       set status = 'abandoned', finished_at = now()
     where player_id = v_player and status = 'active';

    insert into public.acid_games(player_id, solvent, deck_size, status)
    values (v_player, p_solvent, p_deck_size, 'active')
    returning id into v_game;

    return jsonb_build_object('ok', true, 'game_id', v_game);
end;
$$;

create or replace function public.acid_record_move(
    p_course_code text,
    p_session_token text,
    p_game_id uuid,
    p_move_number integer,
    p_optimal boolean
)
returns jsonb
language plpgsql
security definer
set search_path = ''
as $$
declare
    v_player uuid;
begin
    select p.id into v_player
    from public.acid_sessions s
    join public.acid_players p on p.id = s.player_id
    where s.token_hash = encode(extensions.digest(coalesce(p_session_token,''), 'sha256'), 'hex')
      and s.expires_at > now()
      and p.course_code = p_course_code
    limit 1;

    if v_player is null then
        return jsonb_build_object('ok', false, 'error', 'session_expired');
    end if;
    if p_move_number is null or p_move_number < 1 then
        return jsonb_build_object('ok', false, 'error', 'move_invalid');
    end if;
    if not exists (
        select 1 from public.acid_games
        where id = p_game_id and player_id = v_player and status = 'active'
    ) then
        return jsonb_build_object('ok', false, 'error', 'game_not_active');
    end if;

    insert into public.acid_moves(game_id, player_id, optimal, move_number)
    values (p_game_id, v_player, p_optimal, p_move_number)
    on conflict (game_id, move_number) where move_number is not null do nothing;

    return jsonb_build_object('ok', true);
end;
$$;

create or replace function public.acid_finish_game(
    p_course_code text,
    p_session_token text,
    p_game_id uuid,
    p_won boolean
)
returns jsonb
language plpgsql
security definer
set search_path = ''
as $$
declare
    v_player uuid;
begin
    select p.id into v_player
    from public.acid_sessions s
    join public.acid_players p on p.id = s.player_id
    where s.token_hash = encode(extensions.digest(coalesce(p_session_token,''), 'sha256'), 'hex')
      and s.expires_at > now()
      and p.course_code = p_course_code
    limit 1;

    if v_player is null then
        return jsonb_build_object('ok', false, 'error', 'session_expired');
    end if;

    update public.acid_games
       set status = 'completed', won = p_won, finished_at = coalesce(finished_at, now())
     where id = p_game_id and player_id = v_player and status = 'active';

    return jsonb_build_object('ok', true);
end;
$$;

create or replace function public.acid_leaderboard(p_course_code text)
returns table(
    nickname text,
    wins bigint,
    moves bigint,
    optimal_moves bigint,
    optimal_pct numeric
)
language sql
stable
security definer
set search_path = ''
as $$
    select
        p.nickname::text,
        coalesce(g.wins, 0)::bigint as wins,
        coalesce(m.moves, 0)::bigint as moves,
        coalesce(m.optimal_moves, 0)::bigint as optimal_moves,
        case when coalesce(m.moves,0) > 0
             then round(100.0 * m.optimal_moves / m.moves, 1)
             else null end as optimal_pct
    from public.acid_players p
    left join (
        select player_id, count(*) filter (where status='completed' and won is true) as wins
        from public.acid_games
        group by player_id
    ) g on g.player_id = p.id
    left join (
        select player_id,
               count(*) as moves,
               count(*) filter (where optimal is true) as optimal_moves
        from public.acid_moves
        group by player_id
    ) m on m.player_id = p.id
    where p.course_code = p_course_code;
$$;

-- Only the narrow RPC surface is callable from the public browser client.
revoke execute on function public.acid_nickname_allowed(text) from public, anon, authenticated;
revoke execute on function public.acid_create_player(text,text,text) from public, authenticated;
revoke execute on function public.acid_login_player(text,text,text) from public, authenticated;
revoke execute on function public.acid_my_stats(text,text) from public, authenticated;
revoke execute on function public.acid_start_game(text,text,text,text) from public, authenticated;
revoke execute on function public.acid_record_move(text,text,uuid,integer,boolean) from public, authenticated;
revoke execute on function public.acid_finish_game(text,text,uuid,boolean) from public, authenticated;
revoke execute on function public.acid_leaderboard(text) from public, authenticated;

grant execute on function public.acid_create_player(text,text,text) to anon;
grant execute on function public.acid_login_player(text,text,text) to anon;
grant execute on function public.acid_my_stats(text,text) to anon;
grant execute on function public.acid_start_game(text,text,text,text) to anon;
grant execute on function public.acid_record_move(text,text,uuid,integer,boolean) to anon;
grant execute on function public.acid_finish_game(text,text,uuid,boolean) to anon;
grant execute on function public.acid_leaderboard(text) to anon;

-- Ask the Supabase Data API to refresh its function schema immediately.
notify pgrst, 'reload schema';
