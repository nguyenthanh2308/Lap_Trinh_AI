import { useState } from 'react';
import { Sparkles, Copy, AlertCircle, CheckCircle } from 'lucide-react';
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
    <div className="w-full max-w-6xl mx-auto px-4">
      <div className="grid md:grid-cols-2 gap-8">
        {/* Form Section */}
        <div className="flex flex-col">
          <div className="bg-white rounded-lg shadow-lg p-8">
            <h2 className="text-2xl font-bold text-gray-900 mb-6 flex items-center gap-2">
              <Sparkles className="text-blue-500" size={24} />
              Story Details
            </h2>

            <form onSubmit={handleSubmit} className="space-y-5">
              {/* Character Name Input */}
              <div>
                <label htmlFor="name" className="block text-sm font-semibold text-gray-700 mb-2">
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
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent transition outline-none"
                  disabled={loading}
                  aria-label="Character name"
                />
                <p className="text-xs text-gray-500 mt-1">
                  {formData.name.length}/100 characters
                </p>
              </div>

              {/* Personality Input */}
              <div>
                <label htmlFor="personality" className="block text-sm font-semibold text-gray-700 mb-2">
                  Personality Traits
                </label>
                <textarea
                  id="personality"
                  name="personality"
                  value={formData.personality}
                  onChange={handleInputChange}
                  maxLength="100"
                  placeholder="e.g., brave, clever, kind-hearted"
                  rows="3"
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent transition outline-none resize-none"
                  disabled={loading}
                  aria-label="Personality traits"
                />
                <p className="text-xs text-gray-500 mt-1">
                  {formData.personality.length}/100 characters
                </p>
              </div>

              {/* Setting Input */}
              <div>
                <label htmlFor="setting" className="block text-sm font-semibold text-gray-700 mb-2">
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
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent transition outline-none resize-none"
                  disabled={loading}
                  aria-label="Story setting"
                />
                <p className="text-xs text-gray-500 mt-1">
                  {formData.setting.length}/100 characters
                </p>
              </div>

              {/* Theme Input */}
              <div>
                <label htmlFor="theme" className="block text-sm font-semibold text-gray-700 mb-2">
                  Story Theme
                </label>
                <textarea
                  id="theme"
                  name="theme"
                  value={formData.theme}
                  onChange={handleInputChange}
                  maxLength="100"
                  placeholder="e.g., adventure, mystery, romance, fantasy"
                  rows="3"
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent transition outline-none resize-none"
                  disabled={loading}
                  aria-label="Story theme"
                />
                <p className="text-xs text-gray-500 mt-1">
                  {formData.theme.length}/100 characters
                </p>
              </div>

              {/* Buttons */}
              <div className="flex gap-3 pt-4">
                <button
                  type="submit"
                  disabled={loading}
                  className="flex-1 bg-blue-500 hover:bg-blue-600 disabled:bg-gray-400 disabled:cursor-not-allowed text-white font-semibold py-3 px-4 rounded-lg flex items-center justify-center gap-2 transition transform hover:scale-105 disabled:hover:scale-100"
                  aria-label="Generate story"
                >
                  <Sparkles size={18} />
                  {loading ? 'Generating...' : 'Generate Story'}
                </button>

                <button
                  type="button"
                  onClick={handleReset}
                  disabled={loading}
                  className="px-6 bg-gray-200 hover:bg-gray-300 disabled:bg-gray-100 text-gray-700 font-semibold py-3 rounded-lg transition disabled:cursor-not-allowed"
                  aria-label="Reset form"
                >
                  Reset
                </button>
              </div>
            </form>
          </div>
        </div>

        {/* Story Display Section */}
        <div className="flex flex-col">
          <div className="bg-white rounded-lg shadow-lg p-8 flex flex-col h-full">
            <h2 className="text-2xl font-bold text-gray-900 mb-6">Generated Story</h2>

            {/* Error Display */}
            {error && (
              <div className="mb-4 p-4 bg-red-50 border border-red-200 rounded-lg flex gap-3">
                <AlertCircle className="text-red-500 flex-shrink-0" size={20} />
                <div>
                  <p className="text-sm font-semibold text-red-800">Error</p>
                  <p className="text-sm text-red-700">{error}</p>
                </div>
              </div>
            )}

            {/* Loading State */}
            {loading && (
              <div className="flex-1 flex items-center justify-center">
                <div className="text-center">
                  <div className="inline-block">
                    <div className="w-12 h-12 border-4 border-gray-300 border-t-blue-500 rounded-full animate-spin"></div>
                  </div>
                  <p className="mt-4 text-gray-600 font-medium">Generating your story...</p>
                  <p className="text-sm text-gray-500 mt-2">This may take a few seconds</p>
                </div>
              </div>
            )}

            {/* Story Display */}
            {!loading && story && (
              <>
                <div className="flex-1 bg-gray-50 rounded-lg p-6 border border-gray-200 mb-4">
                  <p className="text-gray-800 leading-relaxed whitespace-pre-wrap">{story}</p>
                </div>

                {/* Copy Button */}
                <button
                  onClick={copyToClipboard}
                  className="w-full bg-green-500 hover:bg-green-600 text-white font-semibold py-2 px-4 rounded-lg flex items-center justify-center gap-2 transition transform hover:scale-105"
                  aria-label="Copy story to clipboard"
                >
                  {copySuccess ? (
                    <>
                      <CheckCircle size={18} />
                      Copied!
                    </>
                  ) : (
                    <>
                      <Copy size={18} />
                      Copy to Clipboard
                    </>
                  )}
                </button>
              </>
            )}

            {/* Empty State */}
            {!loading && !story && !error && (
              <div className="flex-1 flex items-center justify-center">
                <div className="text-center text-gray-500">
                  <Sparkles className="mx-auto mb-3 text-gray-400" size={40} />
                  <p className="font-medium">No story yet</p>
                  <p className="text-sm mt-2">Fill in the form and click "Generate Story"</p>
                </div>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
