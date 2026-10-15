import { useEffect, useState } from 'react';
import { api } from '../lib/api';
import { useLang } from '../lib/i18n';
import './CoinShop.css';

interface Benefit {
  slug: string;
  name: string;
  icon: string;
  description: string;
  cost: number;
}

interface Txn {
  amount: number;
  reason: string;
  created_at: string | null;
}

export default function CoinShop() {
  const { t } = useLang();
  const [balance, setBalance] = useState<number | null>(null);
  const [benefits, setBenefits] = useState<Benefit[]>([]);
  const [history, setHistory] = useState<Txn[]>([]);
  const [msg, setMsg] = useState<string>('');
  const [busy, setBusy] = useState<string | null>(null);

  const load = async () => {
    try {
      const b = await api<{ balance: number }>('/coins/mine');
      setBalance(b.balance);
      const ben = await api<{ benefits: Benefit[] }>('/coins/benefits');
      setBenefits(ben.benefits);
      const h = await api<{ transactions: Txn[] }>('/coins/history');
      setHistory(h.transactions);
    } catch {
      setMsg(t('coins.loadError', 'Could not load coin data.'));
    }
  };

  useEffect(() => { load(); }, []);

  const spend = async (benefit: string, cost: number) => {
    if (balance !== null && balance < cost) {
      setMsg(t('coins.notEnough', 'Not enough coins! Keep learning to earn more. 🪙'));
      return;
    }
    setBusy(benefit);
    setMsg('');
    try {
      const r = await api<{ balance: number }>('/coins/spend', {
        method: 'POST',
        body: JSON.stringify({ benefit }),
      });
      setBalance(r.balance);
      setMsg(`✅ ${t('coins.purchased', 'Purchased! Benefit activated.')}`);
      load();
    } catch (e: unknown) {
      const detail = (e as { detail?: string })?.detail;
      setMsg(detail?.includes('need')
        ? t('coins.notEnough', 'Not enough coins! Keep learning to earn more. 🪙')
        : (detail ?? t('coins.error', 'Something went wrong.')));
    } finally {
      setBusy(null);
    }
  };

  return (
    <div className="coin-shop">
      <header className="coin-shop-head">
        <h1>🪙 {t('coins.title', 'Coin Shop')}</h1>
        <div className="coin-balance-big">
          <span className="coin-amount">{balance ?? '–'}</span>
          <span className="coin-label">{t('coins.balance', 'coins')}</span>
        </div>
      </header>

      {msg && <div className="coin-msg" role="status">{msg}</div>}

      <section aria-label="Benefits">
        <h2>{t('coins.spendOn', 'Spend coins on')}</h2>
        <div className="coin-grid">
          {benefits.map((b) => (
            <div key={b.slug} className="coin-card">
              <div className="coin-card-icon">{b.icon}</div>
              <h3>{b.name}</h3>
              <p>{b.description}</p>
              <div className="coin-card-foot">
                <span className="coin-cost">🪙 {b.cost}</span>
                <button
                  className="coin-buy"
                  disabled={busy === b.slug || (balance !== null && balance < b.cost)}
                  onClick={() => spend(b.slug, b.cost)}
                >
                  {busy === b.slug
                    ? '…'
                    : t('coins.buy', 'Get')}
                </button>
              </div>
            </div>
          ))}
        </div>
      </section>

      <section aria-label="History" className="coin-history">
        <h2>{t('coins.history', 'Recent activity')}</h2>
        {history.length === 0 ? (
          <p className="coin-empty">{t('coins.noHistory', 'No transactions yet. Complete tasks to earn coins!')}</p>
        ) : (
          <ul>
            {history.slice(0, 20).map((h, i) => (
              <li key={i} className={h.amount >= 0 ? 'earn' : 'spend'}>
                <span className="txn-amount">{h.amount >= 0 ? '+' : ''}{h.amount} 🪙</span>
                <span className="txn-reason">{h.reason}</span>
                <span className="txn-date">
                  {h.created_at ? new Date(h.created_at).toLocaleDateString() : ''}
                </span>
              </li>
            ))}
          </ul>
        )}
      </section>
    </div>
  );
}
