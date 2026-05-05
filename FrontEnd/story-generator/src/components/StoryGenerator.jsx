import { useState } from 'react';
import {
  Sparkles, Copy, AlertCircle, CheckCircle,
  User, Heart, MapPin, Flame, RotateCcw,
  BookOpen, Loader, Wand2, PenLine,
} from 'lucide-react';
import { useStory } from '../hooks/useStory';

/* ── Field config ── */
const FIELDS = [
  {
    key: 'name',
    label: 'Character Name',
    placeholder: 'e.g., Minh, Anna, Linh…',
    icon: User,
    iconColor: '#a78bfa',
    iconBg: 'rgba(139,92,246,0.15)',
    rows: null,
  },
  {
    key: 'personality',
    label: 'Personality Traits',
    placeholder: 'e.g., brave and curious, quiet but observant…',
    icon: Heart,
    iconColor: '#f472b6',
    iconBg: 'rgba(244,114,182,0.15)',
    rows: 2,
  },
  {
    key: 'setting',
    label: 'Story Setting',
    placeholder: 'e.g., a coastal village, ancient forest, night market…',
    icon: MapPin,
    iconColor: '#34d399',
    iconBg: 'rgba(52,211,153,0.15)',
    rows: 2,
  },
  {
    key: 'theme',
    label: 'Story Theme',
    placeholder: 'e.g., courage, friendship, mystery, hope…',
    icon: Flame,
    iconColor: '#fb923c',
    iconBg: 'rgba(251,146,60,0.15)',
    rows: 2,
  },
];

/* ── Helpers ── */
const EMPTY = { name: '', personality: '', setting: '', theme: '' };

function validate(data) {
  for (const { key, label } of FIELDS) {
    if (!data[key].trim()) return `${label} is required`;
    if (data[key].length > 100) return `${label} must be 100 characters or less`;
  }
  return null;
}

/* ════════════════════════════════════════ */
export default function StoryGenerator() {
  const [formData, setFormData] = useState(EMPTY);
  const [copySuccess, setCopySuccess] = useState(false);
  const [validationError, setValidationError] = useState('');

  const { story, loading, error, generateStory, resetStory } = useStory();

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData((prev) => ({ ...prev, [name]: value }));
    if (validationError) setValidationError('');
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    const err = validate(formData);
    if (err) { setValidationError(err); return; }
    setValidationError('');
    try {
      await generateStory(formData);
      setFormData(EMPTY);
    } catch {/* handled in hook */}
  };

  const handleReset = () => {
    setFormData(EMPTY);
    resetStory();
    setCopySuccess(false);
    setValidationError('');
  };

  const copyToClipboard = async () => {
    try {
      await navigator.clipboard.writeText(story);
      setCopySuccess(true);
      setTimeout(() => setCopySuccess(false), 2500);
    } catch {/* ignore */}
  };

  const hasInput = Object.values(formData).some((v) => v.trim());

  return (
    <div style={{ maxWidth: 1200, margin: '0 auto', padding: '60px 0 40px' }}>

      {/* ── Hero ── */}
      <header className="animate-fadeUp" style={{ textAlign: 'center', marginBottom: 56 }}>
        <div style={{ display: 'inline-flex', alignItems: 'center', gap: 10, marginBottom: 16 }}>
          <span className="badge badge-violet">
            <Sparkles size={11} />
            AI Powered
          </span>
        </div>

        <h1
          className="text-shimmer"
          style={{ fontSize: 'clamp(36px,6vw,64px)', fontWeight: 800, letterSpacing: '-2px', marginBottom: 16 }}
        >
          Story Generator
        </h1>

        <p style={{ fontSize: 18, color: 'var(--text-muted)', maxWidth: 520, margin: '0 auto', lineHeight: 1.6 }}>
          Describe a character and let the AI weave&nbsp;
          <span style={{ color: 'var(--violet-light)', fontWeight: 500 }}>a unique story</span>
          &nbsp;just for you.
        </p>
      </header>

      {/* ── Grid ── */}
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(460px, 1fr))', gap: 24 }}>

        {/* ════ Form Card ════ */}
        <div
          className="card animate-fadeUp"
          style={{ padding: '36px 36px 32px', animationDelay: '0.1s' }}
        >
          {/* Card header */}
          <div style={{ display: 'flex', alignItems: 'center', gap: 12, marginBottom: 28 }}>
            <div style={{
              width: 42, height: 42, borderRadius: 12,
              background: 'var(--grad-primary)',
              display: 'flex', alignItems: 'center', justifyContent: 'center',
              boxShadow: '0 4px 12px rgba(139,92,246,0.4)',
            }}>
              <PenLine size={20} color="#fff" />
            </div>
            <div>
              <h2 style={{ fontSize: 20, fontWeight: 700, color: 'var(--text-primary)', marginBottom: 2 }}>
                Craft Your Story
              </h2>
              <p style={{ fontSize: 13, color: 'var(--text-muted)' }}>
                Fill in the details below to begin
              </p>
            </div>
          </div>

          {/* Validation error */}
          {validationError && (
            <div className="error-banner animate-slideIn" style={{ marginBottom: 20 }}>
              <AlertCircle size={16} color="var(--rose)" style={{ flexShrink: 0, marginTop: 1 }} />
              <p style={{ fontSize: 14, color: '#fda4af', margin: 0 }}>{validationError}</p>
            </div>
          )}

          <form onSubmit={handleSubmit}>
            <div style={{ display: 'flex', flexDirection: 'column', gap: 20 }}>
              {FIELDS.map(({ key, label, placeholder, icon: Icon, iconColor, iconBg, rows }) => (
                <div key={key} className="field-wrapper">
                  <label htmlFor={key} className="field-label">
                    <span className="field-icon" style={{ background: iconBg }}>
                      <Icon size={14} color={iconColor} />
                    </span>
                    {label}
                  </label>

                  {rows ? (
                    <textarea
                      id={key}
                      name={key}
                      className="field-textarea"
                      value={formData[key]}
                      onChange={handleChange}
                      placeholder={placeholder}
                      rows={rows}
                      maxLength={100}
                      disabled={loading}
                      aria-label={label}
                    />
                  ) : (
                    <input
                      id={key}
                      type="text"
                      name={key}
                      className="field-input"
                      value={formData[key]}
                      onChange={handleChange}
                      placeholder={placeholder}
                      maxLength={100}
                      disabled={loading}
                      aria-label={label}
                    />
                  )}

                  <span className="field-counter">
                    {formData[key].length}/100
                  </span>
                </div>
              ))}
            </div>

            {/* Buttons */}
            <div style={{ display: 'flex', gap: 10, marginTop: 28 }}>
              <button
                type="submit"
                className="btn-primary"
                disabled={loading}
                aria-label="Generate story"
              >
                {loading ? (
                  <>
                    <Loader className="animate-spin" size={16} />
                    Generating…
                  </>
                ) : (
                  <>
                    <Wand2 size={16} />
                    Generate Story
                  </>
                )}
              </button>

              {(hasInput || story) && (
                <button
                  type="button"
                  className="btn-secondary"
                  onClick={handleReset}
                  disabled={loading}
                  aria-label="Reset"
                  title="Reset"
                >
                  <RotateCcw size={16} />
                </button>
              )}
            </div>
          </form>
        </div>

        {/* ════ Story Card ════ */}
        <div
          className="card animate-fadeUp"
          style={{ padding: '36px 36px 32px', display: 'flex', flexDirection: 'column', animationDelay: '0.2s' }}
        >
          {/* Card header */}
          <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: 28 }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: 12 }}>
              <div style={{
                width: 42, height: 42, borderRadius: 12,
                background: 'linear-gradient(135deg, rgba(139,92,246,0.3), rgba(99,102,241,0.2))',
                border: '1px solid rgba(139,92,246,0.3)',
                display: 'flex', alignItems: 'center', justifyContent: 'center',
              }}>
                <BookOpen size={20} color="var(--violet-light)" />
              </div>
              <div>
                <h2 style={{ fontSize: 20, fontWeight: 700, color: 'var(--text-primary)', marginBottom: 2 }}>
                  Your Story
                </h2>
                <p style={{ fontSize: 13, color: 'var(--text-muted)' }}>
                  {story ? 'Ready to read' : 'Waiting for input…'}
                </p>
              </div>
            </div>

            {story && !loading && (
              <span className="badge badge-violet animate-fadeIn">
                <Sparkles size={10} />
                Generated
              </span>
            )}
          </div>

          {/* API error */}
          {error && (
            <div className="error-banner animate-slideIn" style={{ marginBottom: 20 }}>
              <AlertCircle size={16} color="var(--rose)" style={{ flexShrink: 0, marginTop: 1 }} />
              <div>
                <p style={{ fontSize: 14, fontWeight: 700, color: '#fda4af', margin: '0 0 3px' }}>
                  Something went wrong
                </p>
                <p style={{ fontSize: 13, color: 'rgba(253,164,175,0.8)', margin: 0 }}>{error}</p>
              </div>
            </div>
          )}

          {/* Loading */}
          {loading && (
            <div className="animate-fadeIn" style={{ flex: 1, display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
              <div style={{ textAlign: 'center' }}>
                <div style={{ position: 'relative', width: 72, height: 72, margin: '0 auto 24px' }}>
                  <div style={{
                    position: 'absolute', inset: 0,
                    border: '3px solid rgba(139,92,246,0.15)',
                    borderTopColor: 'var(--violet)',
                    borderRadius: '50%',
                    animation: 'spin 1s linear infinite',
                  }} />
                  <div style={{
                    position: 'absolute', inset: 8,
                    border: '2px solid rgba(99,102,241,0.15)',
                    borderTopColor: 'var(--indigo)',
                    borderRadius: '50%',
                    animation: 'spin 1.5s linear infinite reverse',
                  }} />
                  <div style={{
                    position: 'absolute', inset: 0,
                    display: 'flex', alignItems: 'center', justifyContent: 'center',
                  }}>
                    <Sparkles size={20} color="var(--violet-light)" />
                  </div>
                </div>

                <p style={{ fontSize: 17, fontWeight: 700, color: 'var(--text-primary)', marginBottom: 8 }}>
                  Weaving your story…
                </p>
                <p style={{ fontSize: 13, color: 'var(--text-muted)', marginBottom: 20 }}>
                  This usually takes 5–30 seconds
                </p>

                <div style={{ display: 'flex', justifyContent: 'center', gap: 8 }}>
                  <div className="loading-dot" />
                  <div className="loading-dot" />
                  <div className="loading-dot" />
                </div>
              </div>
            </div>
          )}

          {/* Story display */}
          {!loading && story && (
            <div className="animate-slideIn" style={{ flex: 1, display: 'flex', flexDirection: 'column', gap: 16 }}>
              <div className="story-parchment" style={{ flex: 1, overflowY: 'auto', maxHeight: 440 }}>
                <p className="story-text">{story}</p>
              </div>

              <button
                onClick={copyToClipboard}
                className={`btn-copy ${copySuccess ? 'copied' : ''}`}
                aria-label="Copy story to clipboard"
              >
                {copySuccess ? (
                  <>
                    <CheckCircle size={15} />
                    Copied to Clipboard!
                  </>
                ) : (
                  <>
                    <Copy size={15} />
                    Copy Story
                  </>
                )}
              </button>
            </div>
          )}

          {/* Empty state */}
          {!loading && !story && !error && (
            <div style={{ flex: 1, display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
              <div style={{ textAlign: 'center' }}>
                <div className="empty-icon-wrapper animate-float">
                  <BookOpen size={32} color="var(--violet-light)" />
                </div>
                <p style={{ fontSize: 16, fontWeight: 600, color: 'var(--text-muted)', marginBottom: 8 }}>
                  No story yet
                </p>
                <p style={{ fontSize: 14, color: 'var(--text-faint)', lineHeight: 1.6 }}>
                  Fill in the form and click&nbsp;
                  <span style={{ color: 'var(--violet-light)', fontWeight: 600 }}>Generate Story</span>
                  &nbsp;to begin
                </p>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
