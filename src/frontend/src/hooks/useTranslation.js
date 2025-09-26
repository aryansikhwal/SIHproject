import { useState, useEffect } from 'react';
import { useLanguage } from '../contexts/LanguageContext';

/**
 * Hook for translating dynamic text (like student names, messages, etc.)
 * @param {string} text - Text to translate
 * @returns {string} - Translated text
 */
export const useTranslateText = (text) => {
  const { td, currentLanguage } = useLanguage();
  const [translatedText, setTranslatedText] = useState(text);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    if (!text || currentLanguage === 'en') {
      setTranslatedText(text);
      return;
    }

    setLoading(true);
    td(text).then(result => {
      setTranslatedText(result);
      setLoading(false);
    }).catch(() => {
      setTranslatedText(text); // Fallback to original text
      setLoading(false);
    });
  }, [text, currentLanguage, td]);

  return { translatedText, loading };
};

/**
 * Hook for translating arrays of text
 * @param {Array<string>} texts - Texts to translate
 * @returns {Object} - { translatedTexts, loading }
 */
export const useTranslateMultiple = (texts) => {
  const { tMultiple, currentLanguage } = useLanguage();
  const [translatedTexts, setTranslatedTexts] = useState(texts);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    if (!texts || texts.length === 0 || currentLanguage === 'en') {
      setTranslatedTexts(texts);
      return;
    }

    setLoading(true);
    tMultiple(texts).then(results => {
      setTranslatedTexts(results);
      setLoading(false);
    }).catch(() => {
      setTranslatedTexts(texts); // Fallback to original texts
      setLoading(false);
    });
  }, [texts, currentLanguage, tMultiple]);

  return { translatedTexts, loading };
};

/**
 * Hook for translating object fields (like student data)
 * @param {Object} obj - Object to translate
 * @param {Array<string>} fieldsToTranslate - Fields that need translation
 * @returns {Object} - { translatedObject, loading }
 */
export const useTranslateObject = (obj, fieldsToTranslate) => {
  const { tObject, currentLanguage } = useLanguage();
  const [translatedObject, setTranslatedObject] = useState(obj);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    if (!obj || !fieldsToTranslate || fieldsToTranslate.length === 0 || currentLanguage === 'en') {
      setTranslatedObject(obj);
      return;
    }

    setLoading(true);
    tObject(obj, fieldsToTranslate).then(result => {
      setTranslatedObject(result);
      setLoading(false);
    }).catch(() => {
      setTranslatedObject(obj); // Fallback to original object
      setLoading(false);
    });
  }, [obj, fieldsToTranslate, currentLanguage, tObject]);

  return { translatedObject, loading };
};

/**
 * Hook for translating arrays of objects (like student lists)
 * @param {Array<Object>} objects - Array of objects to translate
 * @param {Array<string>} fieldsToTranslate - Fields that need translation
 * @returns {Object} - { translatedObjects, loading }
 */
export const useTranslateObjects = (objects, fieldsToTranslate) => {
  const { tObject, currentLanguage } = useLanguage();
  const [translatedObjects, setTranslatedObjects] = useState(objects);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    if (!objects || objects.length === 0 || !fieldsToTranslate || fieldsToTranslate.length === 0 || currentLanguage === 'en') {
      setTranslatedObjects(objects);
      return;
    }

    setLoading(true);
    Promise.all(
      objects.map(obj => tObject(obj, fieldsToTranslate))
    ).then(results => {
      setTranslatedObjects(results);
      setLoading(false);
    }).catch(() => {
      setTranslatedObjects(objects); // Fallback to original objects
      setLoading(false);
    });
  }, [objects, fieldsToTranslate, currentLanguage, tObject]);

  return { translatedObjects, loading };
};
