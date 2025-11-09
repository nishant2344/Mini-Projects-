import numpy as np
import sounddevice as sd
import soundfile as sf
from scipy import signal
from scipy.fft import fft
import pickle
import os
from datetime import datetime

class VoiceRecognitionSystem:
    def __init__(self, sample_rate=22050):
        self.sample_rate = sample_rate
        self.stored_voices = {}
        self.storage_file = "voice_samples.pkl"
        self.load_stored_voices()
    
    def record_audio(self, duration=3):
        """Record audio from microphone"""
        print(f"\n🎤 Recording for {duration} seconds...")
        print("Speak now!")
        
        audio_data = sd.rec(int(duration * self.sample_rate), 
                           samplerate=self.sample_rate, 
                           channels=1, 
                           dtype='float64')
        sd.wait()
        print("✓ Recording complete!")
        
        return audio_data.flatten()
    
    def extract_features(self, audio_data):
        """Extract voice features from audio data"""
        print("\n📊 Extracting features...")
        
        features = {}
        
        # 1. Pitch (Fundamental Frequency)
        features['pitch'] = self.calculate_pitch(audio_data)
        
        # 2. Dominant Frequency
        features['dominant_freq'] = self.calculate_dominant_frequency(audio_data)
        
        # 3. Energy
        features['energy'] = self.calculate_energy(audio_data)
        
        # 4. Zero Crossing Rate
        features['zcr'] = self.calculate_zero_crossing_rate(audio_data)
        
        # 5. Spectral Centroid
        features['spectral_centroid'] = self.calculate_spectral_centroid(audio_data)
        
        # 6. MFCC (Mel-Frequency Cepstral Coefficients)
        features['mfcc'] = self.calculate_mfcc(audio_data)
        
        # 7. RMS (Root Mean Square)
        features['rms'] = np.sqrt(np.mean(audio_data**2))
        
        print("✓ Feature extraction complete!")
        return features
    
    def calculate_pitch(self, audio_data):
        """Calculate average pitch using autocorrelation"""
        correlation = np.correlate(audio_data, audio_data, mode='full')
        correlation = correlation[len(correlation)//2:]
        
        # Find the first peak
        diff = np.diff(correlation)
        start = np.where(diff > 0)[0]
        if len(start) > 0:
            start = start[0]
            peak = np.argmax(correlation[start:]) + start
            pitch = self.sample_rate / peak if peak > 0 else 0
        else:
            pitch = 0
        
        return round(pitch, 2)
    
    def calculate_dominant_frequency(self, audio_data):
        """Calculate dominant frequency using FFT"""
        fft_data = np.abs(fft(audio_data))
        freqs = np.fft.fftfreq(len(audio_data), 1/self.sample_rate)
        
        # Only positive frequencies
        positive_freqs = freqs[:len(freqs)//2]
        positive_fft = fft_data[:len(fft_data)//2]
        
        # Find dominant frequency
        dominant_idx = np.argmax(positive_fft)
        dominant_freq = abs(positive_freqs[dominant_idx])
        
        return round(dominant_freq, 2)
    
    def calculate_energy(self, audio_data):
        """Calculate signal energy"""
        energy = np.sum(audio_data ** 2) / len(audio_data)
        return round(energy, 6)
    
    def calculate_zero_crossing_rate(self, audio_data):
        """Calculate zero crossing rate"""
        zero_crossings = np.sum(np.abs(np.diff(np.sign(audio_data)))) / 2
        zcr = zero_crossings / len(audio_data)
        return round(zcr, 6)
    
    def calculate_spectral_centroid(self, audio_data):
        """Calculate spectral centroid"""
        fft_data = np.abs(fft(audio_data))
        freqs = np.fft.fftfreq(len(audio_data), 1/self.sample_rate)
        
        positive_freqs = freqs[:len(freqs)//2]
        positive_fft = fft_data[:len(fft_data)//2]
        
        if np.sum(positive_fft) > 0:
            centroid = np.sum(positive_freqs * positive_fft) / np.sum(positive_fft)
        else:
            centroid = 0
        
        return round(abs(centroid), 2)
    
    def calculate_mfcc(self, audio_data, n_mfcc=13):
        """Calculate MFCC features (simplified)"""
        # Frame the signal
        frame_length = int(0.025 * self.sample_rate)
        frame_step = int(0.01 * self.sample_rate)
        
        frames = []
        for i in range(0, len(audio_data) - frame_length, frame_step):
            frames.append(audio_data[i:i+frame_length])
        
        if len(frames) == 0:
            return np.zeros(n_mfcc)
        
        # Calculate power spectrum for each frame
        mfcc_features = []
        for frame in frames[:20]:  # Use first 20 frames
            fft_frame = np.abs(fft(frame))
            power_spectrum = fft_frame ** 2
            mfcc_features.append(np.mean(power_spectrum))
        
        # Return mean MFCC values
        return np.mean(mfcc_features) if mfcc_features else 0
    
    def save_voice_sample(self, name, audio_data, features):
        """Save voice sample with features"""
        self.stored_voices[name] = {
            'features': features,
            'audio': audio_data,
            'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        self.save_stored_voices()
        print(f"\n✓ Voice sample for '{name}' saved successfully!")
    
    def compare_voices(self, features):
        """Compare current features with stored voices"""
        if not self.stored_voices:
            print("\n❌ No stored voice samples to compare!")
            return None
        
        print("\n🔍 Comparing with stored voice samples...")
        
        best_match = None
        best_score = float('inf')
        
        for name, data in self.stored_voices.items():
            stored_features = data['features']
            similarity_score = self.calculate_similarity(features, stored_features)
            
            print(f"   - {name}: Similarity = {(1 - similarity_score) * 100:.2f}%")
            
            if similarity_score < best_score:
                best_score = similarity_score
                best_match = name
        
        # Threshold for authentication
        threshold = 0.35
        authenticated = best_score < threshold
        
        print("\n" + "="*50)
        if authenticated:
            print(f"✓ AUTHENTICATION SUCCESSFUL!")
            print(f"   Matched with: {best_match}")
            print(f"   Confidence: {(1 - best_score) * 100:.2f}%")
        else:
            print(f"✗ AUTHENTICATION FAILED!")
            print(f"   Closest match: {best_match}")
            print(f"   Confidence: {(1 - best_score) * 100:.2f}%")
            print(f"   (Below threshold)")
        print("="*50)
        
        return {
            'authenticated': authenticated,
            'match': best_match,
            'score': best_score,
            'confidence': (1 - best_score) * 100
        }
    
    def calculate_similarity(self, features1, features2):
        """Calculate similarity between two feature sets"""
        # Normalize and calculate distance
        weights = {
            'pitch': 0.25,
            'dominant_freq': 0.20,
            'energy': 0.15,
            'zcr': 0.15,
            'spectral_centroid': 0.15,
            'mfcc': 0.10
        }
        
        total_distance = 0
        
        for key in ['pitch', 'dominant_freq', 'spectral_centroid']:
            if features1[key] > 0 and features2[key] > 0:
                diff = abs(features1[key] - features2[key]) / max(features1[key], features2[key])
                total_distance += diff * weights[key]
        
        for key in ['energy', 'zcr', 'mfcc']:
            diff = abs(features1[key] - features2[key])
            total_distance += diff * weights[key]
        
        return total_distance
    
    def display_features(self, features):
        """Display extracted features"""
        print("\n" + "="*50)
        print("EXTRACTED FEATURES:")
        print("="*50)
        print(f"  Pitch (F0):           {features['pitch']} Hz")
        print(f"  Dominant Frequency:   {features['dominant_freq']} Hz")
        print(f"  Energy:               {features['energy']}")
        print(f"  Zero Crossing Rate:   {features['zcr']}")
        print(f"  Spectral Centroid:    {features['spectral_centroid']} Hz")
        print(f"  MFCC:                 {features['mfcc']:.6f}")
        print(f"  RMS:                  {features['rms']:.6f}")
        print("="*50)
    
    def save_stored_voices(self):
        """Save stored voices to file"""
        # Save without audio data (too large)
        save_data = {}
        for name, data in self.stored_voices.items():
            save_data[name] = {
                'features': data['features'],
                'timestamp': data['timestamp']
            }
        
        with open(self.storage_file, 'wb') as f:
            pickle.dump(save_data, f)
    
    def load_stored_voices(self):
        """Load stored voices from file"""
        if os.path.exists(self.storage_file):
            with open(self.storage_file, 'rb') as f:
                save_data = pickle.load(f)
                # Convert loaded data to internal format
                for name, data in save_data.items():
                    self.stored_voices[name] = {
                        'features': data['features'],
                        'timestamp': data['timestamp'],
                        'audio': None  # Audio not saved
                    }
    
    def list_stored_voices(self):
        """List all stored voice samples"""
        if not self.stored_voices:
            print("\n📋 No stored voice samples")
        else:
            print("\n📋 STORED VOICE SAMPLES:")
            print("="*50)
            for i, (name, data) in enumerate(self.stored_voices.items(), 1):
                print(f"{i}. {name}")
                print(f"   Timestamp: {data['timestamp']}")
                print(f"   Pitch: {data['features']['pitch']} Hz")
                print("-"*50)
    
    def delete_voice(self, name):
        """Delete a stored voice sample"""
        if name in self.stored_voices:
            del self.stored_voices[name]
            self.save_stored_voices()
            print(f"\n✓ Voice sample '{name}' deleted!")
        else:
            print(f"\n❌ Voice sample '{name}' not found!")


def main():
    """Main function to run the voice recognition system"""
    vr_system = VoiceRecognitionSystem()
    
    print("="*60)
    print(" "*15 + "VOICE RECOGNITION SYSTEM")
    print("="*60)
    
    while True:
        print("\n📱 MENU:")
        print("1. Record and Save Voice Sample")
        print("2. Record and Authenticate")
        print("3. List Stored Voice Samples")
        print("4. Delete Voice Sample")
        print("5. Exit")
        
        choice = input("\nEnter your choice (1-5): ").strip()
        
        if choice == '1':
            # Record and save
            duration = int(input("Enter recording duration (seconds, default=3): ") or "3")
            audio_data = vr_system.record_audio(duration)
            features = vr_system.extract_features(audio_data)
            vr_system.display_features(features)
            
            name = input("\nEnter name for this voice sample: ").strip()
            if name:
                vr_system.save_voice_sample(name, audio_data, features)
                
                # Optionally save audio file
                save_audio = input("Save audio file? (y/n): ").strip().lower()
                if save_audio == 'y':
                    filename = f"voice_{name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.wav"
                    sf.write(filename, audio_data, vr_system.sample_rate)
                    print(f"✓ Audio saved as '{filename}'")
            else:
                print("❌ Name cannot be empty!")
        
        elif choice == '2':
            # Record and authenticate
            duration = int(input("Enter recording duration (seconds, default=3): ") or "3")
            audio_data = vr_system.record_audio(duration)
            features = vr_system.extract_features(audio_data)
            vr_system.display_features(features)
            vr_system.compare_voices(features)
        
        elif choice == '3':
            # List stored voices
            vr_system.list_stored_voices()
        
        elif choice == '4':
            # Delete voice sample
            vr_system.list_stored_voices()
            name = input("\nEnter name of voice sample to delete: ").strip()
            if name:
                vr_system.delete_voice(name)
        
        elif choice == '5':
            print("\n👋 Thank you for using Voice Recognition System!")
            break
        
        else:
            print("\n❌ Invalid choice! Please try again.")


if __name__ == "__main__":
    main()