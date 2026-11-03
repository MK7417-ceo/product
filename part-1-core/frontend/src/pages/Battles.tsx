import { useCallback, useEffect, useRef, useState } from 'react';
import { useSearchParams } from 'react-router-dom';
import { api } from '../lib/api';
import './battles.css';

// Topics of the curated question bank (queue rejects anything else with
// a clear 400, so this list can only ever shrink a form option, never
// invent a battle).
const TOPICS = [
  'python', 'ml-basics', 'javascript', 'java', 'web-dev', 'networking',
  'data-science', 'data-analyst', 'r', 'ruby', 'devops', 'dsa',
];
const LEVELS = ['beginner', 'intermediate', 'advanced', 'expert'];

interface BattleQuestion {
  id: string;
  prompt: string;
  choices: string[];
  skill: string;
}

interface Battle {
  battle_id: string;
  topic: string;
  bracket: string;
  status: string;
  window_seconds: number;
  player1_id: string;
  player2_id: string | null;
  you_are: string;
  started_at: string | null;
  ends_at: string | null;
  player1_score: number | null;
  player2_score: number | null;
  player1_correct: number | null;
  player2_correct: number | null;
  winner_id: string | null;
  you_won: boolean | null;
  flagged: boolean;
  flag_reason: string;
  rewards: Record<string, unknown>;
  invite_code: string | null;
  submitted: boolean;
  questions?: BattleQuestion[];
  review?: { question_id: string; given: number | null; correct: number | null; is_correct: boolean }[];
}

type Phase = 'loading' | 'lobby' | 'waiting' | 'live' | 'result';

export default function Battles() {
  const [params, setParams] = useSearchParams();
  const [phase, setPhase] = useState<Phase>('loading');
  const [battle, setBattle] = useState<Battle | null>(null);
  const [history, setHistory] = useState<Battle[]>([]);
  const [topic, setTopic] = useState('python');
  const [level, setLevel] = useState('beginner');
  const [windowSeconds, setWindowSeconds] = useState(180);
  const [challengeEmail, setChallengeEmail] = useState('');
  const [inviteCode, setInviteCode] = useState<string | null>(null);
  const [joinCode, setJoinCode] = useState(params.get('invite') || '');
  const [answers, setAnswers] = useState<Record<string, number>>({});
  const [answerTimes, setAnswerTimes] = useState<Record<string, number>>({});
  const [timeLeft, setTimeLeft] = useState(0);
  const [error, setError] = useState('');
  const [busy, setBusy] = useState(false);
  const [fairPlay, setFairPlay] = useState('');
  const startRef = useRef(0);
  const pollRef = useRef<number | null>(null);

  const stopPoll = useCallback(() => {
    if (pollRef.current) window.clearInterval(pollRef.current);
    pollRef.current = null;
  }, []);

  const showBattle = useCallback((b: Battle) => {
    setBattle(b);
    if (b.status === 'live') {
      setPhase(b.submitted ? 'waiting' : 'live');
      if (b.started_at) startRef.current = new Date(b.started_at).getTime();
    } else if (b.status === 'finished') {
      setPhase('result');
    } else {
      setPhase('waiting');
    }
  }, []);

  const refreshMine = useCallback(async () => {
    try {
      const mine = await api<{ battles: Battle[]; open: Battle | null }>('/api/v1/battles/mine');
      setHistory(mine.battles);
      if (mine.open) showBattle(mine.open);
      else if (phase === 'loading') setPhase('lobby');
    } catch {
      setError('Could not load battles. Are you logged in?');
      setPhase('lobby');
    }
  }, [phase, showBattle]);

  useEffect(() => {
    api<{ rules: string }>('/api/v1/battles/fair-play')
      .then((r) => setFairPlay(r.rules))
      .catch(() => undefined);
    refreshMine();
    return stopPoll;
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  // Countdown for a live battle.
  useEffect(() => {
    if (phase !== 'live' || !battle?.ends_at) return;
    const tick = () => {
      const left = Math.max(0, Math.round((new Date(battle.ends_at as string).getTime() - Date.now()) / 1000));
      setTimeLeft(left);
      if (left <= 0) {
        api<Battle>(`/api/v1/battles/${battle.battle_id}`)
          .then(showBattle)
          .catch(() => undefined);
      }
    };
    tick();
    const id = window.setInterval(tick, 1000);
    return () => window.clearInterval(id);
  }, [phase, battle, showBattle]);

  // Poll while waiting for an opponent or for their submission.
  useEffect(() => {
    if (phase !== 'waiting') return;
    if (!battle) return;
    pollRef.current = window.setInterval(async () => {
      try {
        const b = await api<Battle>(`/api/v1/battles/${battle.battle_id}`);
        if (b.status !== 'waiting') {
          stopPoll();
          showBattle(b);
          refreshMine();
        }
      } catch {
        /* keep waiting */
      }
    }, 3000);
    return stopPoll;
  }, [phase, battle, showBattle, stopPoll, refreshMine]);

  const queue = async () => {
    setBusy(true);
    setError('');
    try {
      const r = await api<{ matched: boolean; battle: Battle }>('/api/v1/battles/queue', {
        method: 'POST',
        body: JSON.stringify({ topic, level, window_seconds: windowSeconds }),
      });
      showBattle(r.battle);
      refreshMine();
    } catch (e) {
      setError(e instanceof Error ? e.message : 'Queue failed');
    } finally {
      setBusy(false);
    }
  };

  const challenge = async () => {
    setBusy(true);
    setError('');
    try {
      const r = await api<{ battle: Battle; invite_code: string }>('/api/v1/battles/challenge', {
        method: 'POST',
        body: JSON.stringify({ topic, level, opponent_email: challengeEmail, window_seconds: windowSeconds }),
      });
      setInviteCode(r.invite_code);
      showBattle(r.battle);
      refreshMine();
    } catch (e) {
      setError(e instanceof Error ? e.message : 'Challenge failed');
    } finally {
      setBusy(false);
    }
  };

  const join = async () => {
    setBusy(true);
    setError('');
    try {
      const r = await api<{ battle: Battle }>('/api/v1/battles/join', {
        method: 'POST',
        body: JSON.stringify({ invite_code: joinCode, level }),
      });
      setParams({});
      showBattle(r.battle);
      refreshMine();
    } catch (e) {
      setError(e instanceof Error ? e.message : 'Join failed');
    } finally {
      setBusy(false);
    }
  };

  const pick = (qid: string, idx: number) => {
    setAnswers((a) => ({ ...a, [qid]: idx }));
    setAnswerTimes((t) => {
      if (t[qid] !== undefined) return t;
      const elapsed = Math.max(0, Math.round((Date.now() - startRef.current) / 1000));
      return { ...t, [qid]: elapsed };
    });
  };

  const submit = async () => {
    if (!battle) return;
    if (!window.confirm('Submit your answers? You cannot change them after.')) return;
    setBusy(true);
    setError('');
    try {
      const r = await api<{ battle: Battle; waiting_for_opponent: boolean }>(
        `/api/v1/battles/${battle.battle_id}/submit`,
        { method: 'POST', body: JSON.stringify({ answers, answer_times: answerTimes }) },
      );
      if (r.waiting_for_opponent) {
        setBattle(r.battle);
        setPhase('waiting');
      } else {
        showBattle(r.battle);
      }
      refreshMine();
    } catch (e) {
      setError(e instanceof Error ? e.message : 'Submit failed');
    } finally {
      setBusy(false);
    }
  };

  const rematch = async () => {
    if (!battle) return;
    setBusy(true);
    setError('');
    try {
      const r = await api<{ matched: boolean; battle: Battle }>(
        `/api/v1/battles/${battle.battle_id}/rematch`, { method: 'POST' },
      );
      setAnswers({});
      setAnswerTimes({});
      showBattle(r.battle);
      refreshMine();
    } catch (e) {
      setError(e instanceof Error ? e.message : 'Rematch failed');
    } finally {
      setBusy(false);
    }
  };

  const backToLobby = () => {
    stopPoll();
    setBattle(null);
    setAnswers({});
    setAnswerTimes({});
    setInviteCode(null);
    setPhase('lobby');
    refreshMine();
  };

  const mm = `${Math.floor(timeLeft / 60)}:${String(timeLeft % 60).padStart(2, '0')}`;

  return (
    <div className="battles">
      <h1>⚔️ 1v1 Skill Battles</h1>
      <p className="battles-sub">
        Same questions, same clock, level-matched opponent. Winner takes coins + glory,
        loser still earns practice coins. No bots — every opponent is a real user.
      </p>
      {fairPlay && <p className="battles-fair">{fairPlay}</p>}
      {error && <p className="battles-error">{error}</p>}

      {phase === 'loading' && <p>Loading battles…</p>}

      {phase === 'lobby' && (
        <>
          <div className="battles-card">
            <h2>Find an opponent</h2>
            <label>
              Topic
              <select value={topic} onChange={(e) => setTopic(e.target.value)}>
                {TOPICS.map((t) => <option key={t} value={t}>{t}</option>)}
              </select>
            </label>
            <label>
              Your level
              <select value={level} onChange={(e) => setLevel(e.target.value)}>
                {LEVELS.map((l) => <option key={l} value={l}>{l}</option>)}
              </select>
            </label>
            <label>
              Battle length
              <select value={windowSeconds} onChange={(e) => setWindowSeconds(Number(e.target.value))}>
                <option value={180}>3 minutes</option>
                <option value={240}>4 minutes</option>
                <option value={300}>5 minutes</option>
              </select>
            </label>
            <button disabled={busy} onClick={queue}>⚔️ Queue for battle</button>
            <p className="battles-note">
              Beginners only face beginners, intermediates only intermediates —
              advanced and expert players share the advanced bracket.
            </p>
          </div>

          <div className="battles-card">
            <h2>Challenge a friend</h2>
            <label>
              Friend&apos;s email
              <input
                type="email"
                value={challengeEmail}
                onChange={(e) => setChallengeEmail(e.target.value)}
                placeholder="friend@example.com"
              />
            </label>
            <button disabled={busy || !challengeEmail} onClick={challenge}>Send challenge</button>
            {inviteCode && (
              <p className="battles-note">
                Invite code: <b>{inviteCode}</b> — share this link:{' '}
                <code>{window.location.origin}/battles?invite={inviteCode}</code>
              </p>
            )}
          </div>

          <div className="battles-card">
            <h2>Join with an invite code</h2>
            <label>
              Invite code
              <input value={joinCode} onChange={(e) => setJoinCode(e.target.value)} placeholder="e.g. 3DATNAY1" />
            </label>
            <button disabled={busy || !joinCode} onClick={join}>Join battle</button>
          </div>

          {history.length > 0 && (
            <div className="battles-card">
              <h2>Your battles</h2>
              <ul className="battles-history">
                {history.map((b) => (
                  <li key={b.battle_id}>
                    <button
                      className="battles-history-btn"
                      onClick={() => showBattle(b)}
                    >
                      {b.topic} · {b.bracket} · {b.status}
                      {b.status === 'finished' && b.player1_score !== null &&
                        ` · ${b.player1_score} : ${b.player2_score}`}
                      {b.flagged && ' · ⚠️ flagged'}
                    </button>
                  </li>
                ))}
              </ul>
            </div>
          )}
        </>
      )}

      {phase === 'waiting' && battle && (
        <div className="battles-card">
          <h2>
            {battle.status === 'challenge'
              ? 'Challenge sent — waiting for your friend…'
              : battle.submitted
                ? 'Answers submitted — waiting for your opponent…'
                : 'Waiting for an opponent…'}
          </h2>
          <p className="battles-note">
            {battle.topic} · {battle.bracket} bracket · {battle.window_seconds}s window
          </p>
          {battle.invite_code && (
            <p className="battles-note">
              Invite code: <b>{battle.invite_code}</b> — link:{' '}
              <code>{window.location.origin}/battles?invite={battle.invite_code}</code>
            </p>
          )}
          <p>Checking every few seconds — no need to refresh.</p>
          <button onClick={backToLobby}>Back to lobby</button>
        </div>
      )}

      {phase === 'live' && battle && (
        <div className="battles-card">
          <h2>⚔️ Battle live — {battle.topic} ({battle.bracket})</h2>
          <p className="battles-timer">⏱ Time left: <b>{mm}</b></p>
          {(battle.questions || []).map((q, i) => (
            <div key={q.id} className="battles-q">
              <p><b>Q{i + 1}.</b> {q.prompt}</p>
              <div className="battles-choices">
                {q.choices.map((c, idx) => (
                  <button
                    key={idx}
                    className={answers[q.id] === idx ? 'chosen' : ''}
                    onClick={() => pick(q.id, idx)}
                  >
                    {c}
                  </button>
                ))}
              </div>
            </div>
          ))}
          <button disabled={busy} onClick={submit}>Submit answers</button>
        </div>
      )}

      {phase === 'result' && battle && (
        <div className="battles-card">
          <h2>
            {battle.you_won === null ? '🤝 Draw!' : battle.you_won ? '🏆 You won!' : '💪 You lost — practice XP earned'}
          </h2>
          <p className="battles-score">
            {battle.player1_score} : {battle.player2_score}
            <span> ({battle.player1_correct}/{battle.questions?.length ?? 0} vs {battle.player2_correct}/{battle.questions?.length ?? 0} correct)</span>
          </p>
          {battle.flagged && (
            <p className="battles-error">
              ⚠️ This battle was flagged for review: {battle.flag_reason}. Coins are withheld pending review.
            </p>
          )}
          {!battle.flagged && battle.rewards && (
            <p className="battles-note">
              {battle.you_won === null
                ? 'Draw: both players +5 practice coins.'
                : `Rewards: winner +${String(battle.rewards.winner_coins ?? 0)} coins, loser +${String(battle.rewards.loser_coins ?? battle.rewards.player1_coins ?? 0)} coins.`}
            </p>
          )}
          {battle.review && (
            <div className="battles-review">
              <h3>Review</h3>
              {battle.review.map((r) => (
                <p key={r.question_id}>
                  {r.is_correct ? '✅' : '❌'} Your answer: {r.given ?? '—'} · Correct: {r.correct}
                </p>
              ))}
            </div>
          )}
          <button disabled={busy} onClick={rematch}>🔁 Rematch</button>{' '}
          <button onClick={backToLobby}>Back to lobby</button>
        </div>
      )}
    </div>
  );
}
