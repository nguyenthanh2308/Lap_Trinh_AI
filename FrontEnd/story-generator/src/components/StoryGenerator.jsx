import { useState } from 'react';
import {
  Sparkles,
  Copy,
  AlertCircle,
  CheckCircle,
  User,
  Heart,
  MapPin,
  Flame,
  RotateCcw,
  BookOpen,
  Loader,
} from 'lucide-react';
import { useStory } from '../hooks/useStory';

export default function StoryGenerator() {
  // Form state management
  const [formData, setFormData] = useState({
    name: '',
    personality: '',
    setting: '',
    theme: '',
  });

  const [copySuccess, setCopySuccess] = useState(false);

  // Use the custom hook for story generation
  const { story, loading, error, generateStory, resetStory } = useStory();

  /**
   * Handle input change for form fields
   * @param {Event} e - The input change event
   */
  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData((prev) => ({
      ...prev,
      [name]: value,
    }));
  };

  /**
   * Validate form data
   * @returns {Object} - Validation result with isValid flag and message
   */
  const validateForm = () => {
    const { name, personality, setting, theme } = formData;

    if (!name.trim()) {
      return { isValid: false, message: 'Character name is required' };
    }
    if (!personality.trim()) {
      return { isValid: false, message: 'Personality is required' };
    }
    if (!setting.trim()) {
      return { isValid: false, message: 'Setting is required' };
    }
    if (!theme.trim()) {
      return { isValid: false, message: 'Theme is required' };
    }

    if (name.length > 100) {
      return { isValid: false, message: 'Character name must be 100 characters or less' };
    }
    if (personality.length > 100) {
      return { isValid: false, message: 'Personality must be 100 characters or less' };
    }
    if (setting.length > 100) {
      return { isValid: false, message: 'Setting must be 100 characters or less' };
    }
    if (theme.length > 100) {
      return { isValid: false, message: 'Theme must be 100 characters or less' };
    }

    return { isValid: true, message: '' };
  };

  /**
   * Handle form submission
   * @param {Event} e - The form submit event
   */
  const handleSubmit = async (e) => {
    e.preventDefault();

    // Validate form data
    const validation = validateForm();
    if (!validation.isValid) {
      // Error will be handled by the hook
      return;
    }

    try {
      // Call the generateStory function from the hook
      await generateStory(formData);
      // Reset form on success
      setFormData({
        name: '',
        personality: '',
        setting: '',
        theme: '',
      });
    } catch (err) {
      // Error is handled in the hook
      console.error('Story generation failed:', err);
    }
  };

  /**
   * Handle reset - clear form and story
   */
  const handleReset = () => {
    setFormData({
      name: '',
      personality: '',
      setting: '',
      theme: '',
    });
    resetStory();
    setCopySuccess(false);
  };

  /**
   * Copy story to clipboard
   */
  const copyToClipboard = async () => {
    try {
      await navigator.clipboard.writeText(story);
      setCopySuccess(true);
      setTimeout(() => setCopySuccess(false), 2000);
    } catch (err) {
      console.error('Failed to copy:', err);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 via-blue-50 to-indigo-50 py-12 px-4">
      <div className="max-w-7xl mx-auto">
        {/* Hero Section */}
        <div className="text-center mb-12">
          <div className="flex items-center justify-center gap-3 mb-4">
            <BookOpen className="text-indigo-600" size={32} />
            <h1 className="text-5xl font-bold bg-gradient-to-r from-indigo-600 to-purple-600 bg-clip-text text-transparent">
              Story Generator
            </h1>
            <Sparkles className="text-amber-400" size={32} />
          </div>
          <p className="text-xl text-gray-600 max-w-2xl mx-auto">
            Create captivating stories with AI. Fill in the details and let imagination flow.
          </p>
        </div>

        {/* Main Content Grid */}
        <div className="grid lg:grid-cols-2 gap-8">
          {/* Form Section */}
          <div className="flex flex-col">
            <div className="bg-white/80 backdrop-blur-sm rounded-2xl shadow-xl p-8 h-full border border-white/50">
              {/* Form Header */}
              <div className="mb-8">
                <h2 className="text-2xl font-bold text-gray-900 flex items-center gap-2">
                  <Sparkles className="text-indigo-600" size={24} />
                  Craft Your Story
                </h2>
                <p className="text-sm text-gray-500 mt-2">Tell us the details and let AI weave the narrative</p>
              </div>

              <form onSubmit={handleSubmit} className="space-y-6">
                {/* Character Name Input */}
                <div className="group">
                  <label htmlFor="name" className="block text-sm font-semibold text-gray-700 mb-2 flex items-center gap-2">
                    <User className="text-indigo-500" size={18} />
                    Character Name
                  </label>
                  <input
                    id="name"
                    type="text"
                    name="name"
                    value={formData.name}
                    onChange={handleInputChange}
                    maxLength="100"
                    placeholder="e.g., Minh, Anna, Thao"
                    className="w-full px-4 py-3 border-2 border-gray-200 rounded-lg focus:border-indigo-500 focus:ring-2 focus:ring-indigo-200 transition outline-none bg-gray-50 group-hover:bg-white disabled:bg-gray-100 disabled:cursor-not-allowed"
                    disabled={loading}
                    aria-label="Character name"
                  />
                  <p className="text-xs text-gray-500 mt-1.5 font-medium">
                    {formData.name.length}/100 characters
                  </p>
                </div>

                {/* Personality Input */}
                <div className="group">
                  <label htmlFor="personality" className="block text-sm font-semibold text-gray-700 mb-2 flex items-center gap-2">
                    <Heart className="text-pink-500" size={18} />
                    Personality Traits
                  </label>
                  <textarea
                    id="personality"
                    name="personality"
                    value={formData.personality}
                    onChange={handleInputChange}
                    maxLength="100"
                    placeholder="e.g., brave, clever, kind-hearted, mysterious"
                    rows="3"
                    className="w-full px-4 py-3 border-2 border-gray-200 rounded-lg focus:border-indigo-500 focus:ring-2 focus:ring-indigo-200 transition outline-none resize-none bg-gray-50 group-hover:bg-white disabled:bg-gray-100 disabled:cursor-not-allowed"
                    disabled={loading}
                    aria-label="Personality traits"
                  />
                  <p className="text-xs text-gray-500 mt-1.5 font-medium">
                    {formData.personality.length}/100 characters
                  </p>
                </div>

                {/* Setting Input */}
                <div className="group">
                  <label htmlFor="setting" className="block text-sm font-semibold text-gray-700 mb-2 flex items-center gap-2">
                    <MapPin className="text-green-500" size={18} />
                    Story Setting
                  </label>
                  <textarea
                    id="setting"
                    name="setting"
                    value={formData.setting}
                    onChange={handleInputChange}
                    maxLength="100"
                    placeholder="e.g., a coastal village, ancient forest, futuristic city"
                    rows="3"
                    className="w-full px-4 py-3 border-2 border-gray-200 rounded-lg focus:border-indigo-500 focus:ring-2 focus:ring-indigo-200 transition outline-none resize-none bg-gray-50 group-hover:bg-white disabled:bg-gray-100 disabled:cursor-not-allowed"
                    disabled={loading}
                    aria-label="Story setting"
                  />
                  <p className="text-xs text-gray-500 mt-1.5 font-medium">
                    {formData.setting.length}/100 characters
                  </p>
                </div>

                {/* Theme Input */}
                <div className="group">
                  <label htmlFor="theme" className="block text-sm font-semibold text-gray-700 mb-2 flex items-center gap-2">
                    <Flame className="text-orange-500" size={18} />
                    Story Theme
                  </label>
                  <textarea
                    id="theme"
                    name="theme"
                    value={formData.theme}
                    onChange={handleInputChange}
                    maxLength="100"
                    placeholder="e.g., adventure, mystery, romance, fantasy, sci-fi"
                    rows="3"
                    className="w-full px-4 py-3 border-2 border-gray-200 rounded-lg focus:border-indigo-500 focus:ring-2 focus:ring-indigo-200 transition outline-none resize-none bg-gray-50 group-hover:bg-white disabled:bg-gray-100 disabled:cursor-not-allowed"
                    disabled={loading}
                    aria-label="Story theme"
                  />
                  <p className="text-xs text-gray-500 mt-1.5 font-medium">
                    {formData.theme.length}/100 characters
                  </p>
                </div>

                {/* Buttons */}
                <div className="flex gap-3 pt-2">
                  <button
                    type="submit"
                    disabled={loading}
                    className="flex-1 relative bg-gradient-to-r from-indigo-600 to-purple-600 hover:from-indigo-700 hover:to-purple-700 disabled:from-gray-400 disabled:to-gray-500 disabled:cursor-not-allowed text-white font-semibold py-3 px-4 rounded-xl flex items-center justify-center gap-2 transition-all transform hover:shadow-lg hover:scale-105 disabled:hover:scale-100 disabled:shadow-none"
                    aria-label="Generate story"
                  >
                    {loading ? (
                      <>
                        <Loader className="animate-spin" size={18} />
                        Generating...
                      </>
                    ) : (
                      <>
                        <Sparkles size={18} />
                        Generate Story
                      </>
                    )}
                  </button>

                  <button
                    type="button"
                    onClick={handleReset}
                    disabled={loading}
                    className="px-6 bg-gray-100 hover:bg-gray-200 disabled:bg-gray-50 text-gray-700 font-semibold py-3 rounded-xl transition-all transform hover:scale-105 disabled:hover:scale-100 disabled:cursor-not-allowed border border-gray-300 hover:border-gray-400"
                    aria-label="Reset form"
                  >
                    <RotateCcw size={18} />
                  </button>
                </div>
              </form>
            </div>
          </div>

          {/* Story Display Section */}
          <div className="flex flex-col">
            <div className="bg-white/80 backdrop-blur-sm rounded-2xl shadow-xl p-8 h-full flex flex-col border border-white/50">
              {/* Display Header */}
              <div className="mb-6">
                <h2 className="text-2xl font-bold text-gray-900 flex items-center gap-2">
                  <BookOpen className="text-purple-600" size={24} />
                  Your Story
                </h2>
              </div>

              {/* Error Display */}
              {error && (
                <div className="mb-6 p-4 bg-gradient-to-r from-red-50 to-orange-50 border-2 border-red-200 rounded-xl flex gap-3 animate-slideIn">
                  <AlertCircle className="text-red-500 flex-shrink-0 mt-0.5" size={20} />
                  <div>
                    <p className="text-sm font-bold text-red-900">Oops! Something went wrong</p>
                    <p className="text-sm text-red-700 mt-1">{error}</p>
                  </div>
                </div>
              )}

              {/* Loading State */}
              {loading && (
                <div className="flex-1 flex items-center justify-center animate-fadeIn">
                  <div className="text-center">
                    <div className="inline-block mb-6">
                      <div className="w-16 h-16 border-4 border-gray-200 border-t-indigo-600 rounded-full animate-spin"></div>
                    </div>
                    <p className="text-lg font-bold text-gray-900 mb-2">The AI is writing your story...</p>
                    <p className="text-sm text-gray-500">This usually takes 5-30 seconds depending on GPU power</p>
                    <div className="mt-4 flex justify-center gap-2">
                      <div className="w-2 h-2 bg-indigo-600 rounded-full animate-bounce" style={{ animationDelay: '0s' }}></div>
                      <div className="w-2 h-2 bg-indigo-600 rounded-full animate-bounce" style={{ animationDelay: '0.2s' }}></div>
                      <div className="w-2 h-2 bg-indigo-600 rounded-full animate-bounce" style={{ animationDelay: '0.4s' }}></div>
                    </div>
                  </div>
                </div>
              )}

              {/* Story Display */}
              {!loading && story && (
                <div className="flex-1 flex flex-col animate-slideIn">
                  <div className="flex-1 bg-gradient-to-br from-amber-50 to-orange-50 rounded-xl p-8 border-2 border-amber-100 mb-6 overflow-y-auto">
                    <p
                      className="text-gray-800 leading-relaxed whitespace-pre-wrap"
                      style={{
                        fontFamily: "'Georgia', 'Garamond', serif",
                        fontSize: '1.1rem',
                        lineHeight: '1.8',
                      }}
                    >
                      {story}
                    </p>
                  </div>

                  {/* Copy Button */}
                  <button
                    onClick={copyToClipboard}
                    className={`w-full font-semibold py-3 px-4 rounded-xl flex items-center justify-center gap-2 transition-all transform hover:scale-105 ${
                      copySuccess
                        ? 'bg-green-500 hover:bg-green-600 text-white'
                        : 'bg-indigo-600 hover:bg-indigo-700 text-white'
                    }`}
                    aria-label="Copy story to clipboard"
                  >
                    {copySuccess ? (
                      <>
                        <CheckCircle size={18} />
                        Copied to Clipboard!
                      </>
                    ) : (
                      <>
                        <Copy size={18} />
                        Copy Story
                      </>
                    )}
                  </button>
                </div>
              )}

              {/* Empty State */}
              {!loading && !story && !error && (
                <div className="flex-1 flex items-center justify-center">
                  <div className="text-center">
                    <div className="mb-4">
                      <BookOpen className="mx-auto text-gray-300" size={56} />
                    </div>
                    <p className="text-lg font-semibold text-gray-600 mb-2">No story yet</p>
                    <p className="text-sm text-gray-500">
                      Fill in the form on the left and click<br />
                      <span className="font-semibold">"Generate Story"</span> to begin
                    </p>
                  </div>
                </div>
              )}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
