class SoundEffects {
  constructor() {
    this.enabled = localStorage.getItem('soundEnabled') !== 'false';
    this.audioContext = null;
  }
  init() {
    if (!this.audioContext) {
      this.audioContext = new (window.AudioContext || window.webkitAudioContext)();
    }
  }
  playTone(frequency, duration, type = 'sine') {
    if (!this.enabled) return;
    try {
      this.init();
      const oscillator = this.audioContext.createOscillator();
      const gainNode = this.audioContext.createGain();
      oscillator.connect(gainNode);
      gainNode.connect(this.audioContext.destination);
      oscillator.frequency.value = frequency;
      oscillator.type = type;
      gainNode.gain.setValueAtTime(0.1, this.audioContext.currentTime);
      gainNode.gain.exponentialRampToValueAtTime(0.01, this.audioContext.currentTime + duration);
      oscillator.start(this.audioContext.currentTime);
      oscillator.stop(this.audioContext.currentTime + duration);
    } catch (error) {
    }
  }
  sendMessage() {
    this.playTone(400, 0.1);
    setTimeout(() => this.playTone(600, 0.1), 50);
  }
  receiveMessage() {
    this.playTone(800, 0.15);
    setTimeout(() => this.playTone(1000, 0.1), 100);
  }
  error() {
    this.playTone(300, 0.2);
    setTimeout(() => this.playTone(200, 0.2), 100);
  }
  toggle() {
    this.enabled = !this.enabled;
    localStorage.setItem('soundEnabled', this.enabled);
    if (this.enabled) {
      this.receiveMessage();
    }
    return this.enabled;
  }
  isEnabled() {
    return this.enabled;
  }
}
export default new SoundEffects();