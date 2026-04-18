import StoryGenerator from './components/StoryGenerator'
import './App.css'

function App() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 py-12">
      {/* Header */}
      <header className="mb-12">
        <div className="container mx-auto px-4">
          <h1 className="text-5xl font-bold text-center text-gray-900 mb-2">
            ✨ AI Short Story Generator
          </h1>
          <p className="text-center text-gray-600 text-lg">
            Create unique Vietnamese stories powered by artificial intelligence
          </p>
        </div>
      </header>

      {/* Main Content */}
      <main className="container mx-auto px-4 mb-12">
        <StoryGenerator />
      </main>

      {/* Footer */}
      <footer className="border-t border-gray-200 bg-white bg-opacity-50">
        <div className="container mx-auto px-4 py-8 text-center text-gray-600">
          <p>
            Backend API: <code className="bg-gray-100 px-2 py-1 rounded">http://localhost:8000</code>
          </p>
          <p className="mt-2 text-sm">
            Built with React, Vite, Tailwind CSS, and Lucide Icons
          </p>
        </div>
      </footer>
    </div>
  )
}

export default App
