# 3M Lighting Consumer Video Analysis - Configuration
# Updated: October 21, 2025

PROCESSING_CONFIG = {
    # Processing tier: FREE (local only), PLUS (hybrid), PRO (max quality)
    'tier': 'PLUS',
    
    # Minimum confidence threshold for including insights (0.0 to 1.0)
    'confidence_threshold': 0.75,
    
    # Priority questions from discussion guide (1-11)
    'priority_questions': [3, 7, 8],
    
    # Focus areas (ranked by importance)
    'focus_areas': [
        'pain_points',
        '3m_adjacency',
        'golden_moments',
        'workarounds'
    ],
    
    # Emotion sensitivity: low, medium, high
    'emotion_sensitivity': 'high',
    
    # Quote selection preference: 'impactful' or 'representative'
    'quote_preference': 'impactful',
    
    # Video processing settings
    'frame_sample_interval': 5,  # seconds between frame samples
    'emotion_window': 5,  # seconds for emotion-JTBD alignment
    
    # Output settings
    'max_quotes_per_category': 20,
    'max_pain_points': 7,
    'generate_html_visualization': True
}

# Model paths
MODEL_PATHS = {
    'qwen': '/Volumes/TARS/llm-models/qwen2.5-vl-7b-instruct',
    'whisper': 'large-v3-turbo',
    'hubert': '/Volumes/TARS/llm-models/hubert-large'
}

# Directory structure
PATHS = {
    'raw_videos': '/Volumes/DATA/consulting/3m-lighting-processed/raw_videos',
    'processed': '/Volumes/DATA/consulting/3m-lighting-processed/processed',
    'outputs': '/Volumes/DATA/consulting/3m-lighting-processed/outputs',
    'logs': '/Volumes/DATA/consulting/3m-lighting-processed/logs'
}
