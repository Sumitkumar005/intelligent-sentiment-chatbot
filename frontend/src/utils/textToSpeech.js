class TextToSpeech {
  constructor() {
    const savedState = localStorage.getItem('ttsEnabled');
    this.enabled = savedState === null ? true : savedState === 'true';
    this.synth = window.speechSynthesis;
    this.voice = null;
    this.initVoices();
  }
  initVoices() {
    const loadVoices = () => {
      this.voices = this.synth.getVoices();
    };
    loadVoices();
    if (this.synth.onvoiceschanged !== undefined) {
      this.synth.onvoiceschanged = loadVoices;
    }
  }
  getVoiceForLanguage(langCode) {
    if (!this.voices || this.voices.length === 0) {
      this.voices = this.synth.getVoices();
    }
    const langMap = {
      'en': 'en',      
      'es': 'es',      
      'fr': 'fr',      
      'de': 'de',      
      'zh': 'zh',      
      'ja': 'ja',      
      'hi': 'hi',      
      'ar': 'ar'       
    };
    const targetLang = langMap[langCode] || 'en';
    const voice = this.voices.find(v => v.lang.startsWith(targetLang));
    if (voice) {
    } else {
    }
    return voice || this.voices[0];
  }
  speak(text, langCode = 'en') {
    if (!this.enabled || !text) {
      return;
    }
    this.synth.cancel();
    const utterance = new SpeechSynthesisUtterance(text);
    const voice = this.getVoiceForLanguage(langCode);
    if (voice) {
      utterance.voice = voice;
      utterance.lang = voice.lang;
    }
    utterance.rate = 1.0; 
    utterance.pitch = 1.0; 
    utterance.volume = 1.0; 
    utterance.onerror = (event) => {
    };
    utterance.onstart = () => {
    };
    utterance.onend = () => {
    };
    this.synth.speak(utterance);
  }
  stop() {
    this.synth.cancel();
  }
  toggle() {
    this.enabled = !this.enabled;
    localStorage.setItem('ttsEnabled', this.enabled);
    if (!this.enabled) {
      this.stop();
    }
    return this.enabled;
  }
  isEnabled() {
    return this.enabled;
  }
  isSupported() {
    return 'speechSynthesis' in window;
  }
}
export default new TextToSpeech();