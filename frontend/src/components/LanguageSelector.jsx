import React, { useState } from 'react';
import './LanguageSelector.css';
const LanguageSelector = ({ currentLang, onLanguageChange }) => {
  const [showDropdown, setShowDropdown] = useState(false);
  const languages = [
    { code: 'en', name: 'English', flag: '🇺🇸' },
    { code: 'es', name: 'Español', flag: '🇪🇸' },
    { code: 'fr', name: 'Français', flag: '🇫🇷' },
    { code: 'de', name: 'Deutsch', flag: '🇩🇪' },
    { code: 'zh', name: '中文', flag: '🇨🇳' },
    { code: 'ja', name: '日本語', flag: '🇯🇵' },
    { code: 'hi', name: 'हिन्दी', flag: '🇮🇳' },
    { code: 'ar', name: 'العربية', flag: '🇸🇦' }
  ];
  const currentLanguage = languages.find(lang => lang.code === currentLang) || languages[0];
  const handleSelect = (langCode) => {
    onLanguageChange(langCode);
    setShowDropdown(false);
  };
  return (
    <div className="language-selector">
      <button
        className="language-btn"
        onClick={() => setShowDropdown(!showDropdown)}
        title="Change language"
      >
        <span className="lang-flag">{currentLanguage.flag}</span>
      </button>
      {showDropdown && (
        <>
          <div className="language-backdrop" onClick={() => setShowDropdown(false)} />
          <div className="language-dropdown">
            {languages.map((lang) => (
              <button
                key={lang.code}
                className={`language-option ${lang.code === currentLang ? 'active' : ''}`}
                onClick={() => handleSelect(lang.code)}
              >
                <span className="lang-flag">{lang.flag}</span>
                <span className="lang-name">{lang.name}</span>
                {lang.code === currentLang && <span className="check-mark">✓</span>}
              </button>
            ))}
          </div>
        </>
      )}
    </div>
  );
};
export default LanguageSelector;