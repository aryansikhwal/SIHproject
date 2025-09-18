import React, { useState } from 'react';
import { useLanguage } from '../contexts/LanguageContext';
import { useTranslateText } from '../hooks/useTranslation';
import { MessageCircle, Send } from 'lucide-react';

const TranslationDemo = () => {
  const { t, currentLanguage } = useLanguage();
  const [inputText, setInputText] = useState('');
  const [textToTranslate, setTextToTranslate] = useState('Welcome to AttenSync! This message will be automatically translated.');
  
  const { translatedText, loading } = useTranslateText(textToTranslate);

  const handleTranslate = () => {
    if (inputText.trim()) {
      setTextToTranslate(inputText.trim());
      setInputText('');
    }
  };

  const sampleTexts = [
    'Good morning students! Please take your seats.',
    'Assignment submission deadline is tomorrow.',
    'Parent-teacher meeting scheduled for next Friday.',
    'Congratulations on your excellent performance!',
    'Please bring your textbooks to class.'
  ];

  return (
    <div className="bg-white rounded-2xl p-6 shadow-lg">
      <div className="flex items-center mb-4">
        <MessageCircle className="h-6 w-6 text-primary mr-2" />
        <h3 className="text-xl font-semibold text-neutral-dark">
          {t('language')} Translation Demo
        </h3>
      </div>
      
      <div className="space-y-4">
        {/* Current Language Display */}
        <div className="p-3 bg-gray-50 rounded-lg">
          <p className="text-sm text-gray-600">
            Current Language: <span className="font-semibold text-primary">{currentLanguage.toUpperCase()}</span>
          </p>
        </div>

        {/* Translation Result */}
        <div className="p-4 border-2 border-primary-light rounded-lg">
          <p className="text-sm text-gray-600 mb-2">Translated Text:</p>
          {loading ? (
            <div className="flex items-center space-x-2">
              <div className="h-4 w-4 animate-spin rounded-full border-2 border-primary border-t-transparent"></div>
              <span className="text-sm text-gray-500">Translating...</span>
            </div>
          ) : (
            <p className="text-lg text-neutral-dark">{translatedText}</p>
          )}
        </div>

        {/* Input for Custom Translation */}
        <div className="flex space-x-2">
          <input
            type="text"
            value={inputText}
            onChange={(e) => setInputText(e.target.value)}
            placeholder="Enter text to translate..."
            className="flex-1 p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary focus:border-transparent"
            onKeyPress={(e) => e.key === 'Enter' && handleTranslate()}
          />
          <button
            onClick={handleTranslate}
            disabled={!inputText.trim()}
            className="px-4 py-3 bg-primary text-white rounded-lg hover:bg-green-700 disabled:bg-gray-300 transition-colors"
          >
            <Send className="h-4 w-4" />
          </button>
        </div>

        {/* Sample Texts */}
        <div>
          <p className="text-sm font-medium text-gray-700 mb-2">Try these samples:</p>
          <div className="flex flex-wrap gap-2">
            {sampleTexts.map((sample, index) => (
              <button
                key={index}
                onClick={() => setTextToTranslate(sample)}
                className="px-3 py-1 text-sm bg-gray-100 hover:bg-gray-200 rounded-full transition-colors"
              >
                {sample.substring(0, 30)}...
              </button>
            ))}
          </div>
        </div>

        {/* Features List */}
        <div className="mt-6 p-4 bg-green-50 rounded-lg">
          <h4 className="font-semibold text-green-800 mb-2">🌟 Auto-Translation Features:</h4>
          <ul className="text-sm text-green-700 space-y-1">
            <li>• Student names and messages are auto-translated</li>
            <li>• Real-time translation as you switch languages</li>
            <li>• Cached translations for better performance</li>
            <li>• Works offline with fallback to original text</li>
            <li>• Perfect for rural schools with multiple languages</li>
          </ul>
        </div>
      </div>
    </div>
  );
};

export default TranslationDemo;
