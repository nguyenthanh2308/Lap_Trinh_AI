import StoryGenerator from './components/StoryGenerator'
import './App.css'

function App() {
  return (
    <div className="app-wrapper">
      {/* Background orbs */}
      <div className="bg-orb bg-orb-1" />
      <div className="bg-orb bg-orb-2" />
      <div className="bg-orb bg-orb-3" />

      {/* Content */}
      <div style={{ position: 'relative', zIndex: 1, minHeight: '100svh', display: 'flex', flexDirection: 'column' }}>
        <main style={{ flex: 1, padding: '0 16px' }}>
          <StoryGenerator />
        </main>

        {/* Footer */}
        <footer style={{
          borderTop: '1px solid rgba(255,255,255,0.06)',
          padding: '20px 24px',
          textAlign: 'center',
          color: 'var(--text-faint)',
          fontSize: '13px',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          gap: '12px',
          flexWrap: 'wrap',
        }}>
          <span>AI Short Story Generator</span>
          <span style={{ color: 'rgba(255,255,255,0.1)' }}>·</span>
          <span>Built with React + FastAPI + GPT-2</span>
          <span style={{ color: 'rgba(255,255,255,0.1)' }}>·</span>
          <code style={{
            background: 'rgba(139,92,246,0.12)',
            border: '1px solid rgba(139,92,246,0.25)',
            color: 'var(--violet-light)',
            padding: '2px 10px',
            borderRadius: '6px',
            fontSize: '12px',
            fontFamily: 'var(--font-sans)',
          }}>
            localhost:8000
          </code>
        </footer>
      </div>
    </div>
  )
}

export default App
