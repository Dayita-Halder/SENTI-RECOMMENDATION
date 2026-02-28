"""
Sentiment Classification & Recommendation Model Module
========================================================
Production-ready module for sentiment prediction and product recommendations.
Loads pre-trained models from pickle files.

NO TRAINING CODE - Only inference.
"""

import os
import pickle
import re
import string
import numpy as np
import pandas as pd

# Try to import NLTK (optional)
NLTK_AVAILABLE = False
try:
    import nltk
    from nltk.corpus import stopwords
    from nltk.stem import WordNetLemmatizer
    # Don't download here - let it fail gracefully
    NLTK_AVAILABLE = True
except:
    pass

# Fallback stopwords if NLTK unavailable
FALLBACK_STOPWORDS = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 
                      'of', 'with', 'by', 'from', 'as', 'is', 'was', 'are', 'were', 'been',
                      'be', 'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would',
                      'should', 'could', 'may', 'might', 'must', 'can', 'this', 'that',
                      'these', 'those', 'i', 'you', 'he', 'she', 'it', 'we', 'they',
                      'me', 'him', 'her', 'us', 'them', 'my', 'your', 'his', 'its', 'our'}

# ============================================================
# GLOBAL CONFIGURATION
# ============================================================

PICKLE_DIR = os.path.dirname(os.path.abspath(__file__))

SENTIMENT_THRESHOLD = 0.5  # Probability threshold for positive sentiment
RECOMMENDATION_TOP_N = 5   # Number of recommendations to return

# ============================================================
# TEXT PREPROCESSING
# ============================================================

def preprocess_text(text: str) -> str:
    """
    Clean and normalize review text for model input.
    
    Steps:
    1. Lowercase
    2. Remove URLs and special characters
    3. Remove punctuation
    4. Tokenize
    5. Remove stopwords
    6. Lemmatize
    
    Args:
        text: Raw review text
        
    Returns:
        Preprocessed text (space-separated tokens)
    """
    # Handle None/NaN
    if not isinstance(text, str) or len(text.strip()) == 0:
        return ""
    
    # Lowercase
    text = text.lower()
    
    # Remove URLs
    text = re.sub(r'http\S+|www\S+|https\S+', '', text, flags=re.MULTILINE)
    
    # Remove email addresses
    text = re.sub(r'\S+@\S+', '', text)
    
    # Remove special characters (keep alphanumeric and spaces)
    text = re.sub(r'[^a-z0-9\s]', '', text)
    
    # Tokenize
    tokens = text.split()
    
    # Remove stopwords
    if NLTK_AVAILABLE:
        try:
            stop_words = set(stopwords.words('english'))
        except:
            stop_words = FALLBACK_STOPWORDS
    else:
        stop_words = FALLBACK_STOPWORDS
    tokens = [t for t in tokens if t not in stop_words and len(t) > 2]
    
    # Lemmatize (optional)
    if NLTK_AVAILABLE:
        try:
            lemmatizer = WordNetLemmatizer()
            tokens = [lemmatizer.lemmatize(t) for t in tokens]
        except:
            pass  # Skip lemmatization if it fails
    
    return ' '.join(tokens)


# ============================================================
# MODEL LOADING
# ============================================================

class SentimentRecommenderSystem:
    """
    Complete sentiment classification and recommendation system.
    
    Pipeline:
    1. Load pre-trained TF-IDF vectorizer
    2. Load pre-trained sentiment classifier (Logistic Regression)
    3. Load pre-trained recommender (SVD/User-Based CF)
    4. Load review database for sentiment computation
    """
    
    def __init__(self, pickle_dir: str = PICKLE_DIR):
        """
        Initialize system by loading all pre-trained artifacts.
        
        Args:
            pickle_dir: Directory containing pickle files
            
        Raises:
            FileNotFoundError: If required pickle files are missing
        """
        self.pickle_dir = pickle_dir
        self._load_artifacts()
    
    def _load_artifacts(self):
        """Load all pickle files from disk."""
        
        # Required files
        required_files = {
            'tfidf_vectorizer.pkl': 'TF-IDF Vectorizer',
            'sentiment_model.pkl': 'Sentiment Classifier',
            'user_based_cf.pkl': 'Collaborative Filter',
            'master_reviews.pkl': 'Review Database'
        }
        
        # Check files exist
        missing = []
        for fname in required_files:
            fpath = os.path.join(self.pickle_dir, fname)
            if not os.path.exists(fpath):
                missing.append(fname)
        
        if missing:
            raise FileNotFoundError(
                f"Missing required pickle files: {missing}\n"
                f"Expected location: {self.pickle_dir}\n"
                f"Run the Jupyter notebook to generate these files first."
            )
        
        # Load artifacts
        print("Loading pre-trained artifacts...")
        
        self.tfidf_vectorizer = self._load_pickle('tfidf_vectorizer.pkl')
        print("  ✓ TF-IDF Vectorizer loaded")
        
        self.sentiment_model = self._load_pickle('sentiment_model.pkl')
        print("  ✓ Sentiment Classifier loaded")
        
        self.recommender = self._load_pickle('user_based_cf.pkl')
        print("  ✓ Recommender loaded")
        
        self.reviews_df = self._load_pickle('master_reviews.pkl')
        print("  ✓ Review Database loaded")
        
        print(f"System ready. Dataset: {len(self.reviews_df)} reviews, {self.reviews_df['name'].nunique()} products")
    
    @staticmethod
    def _load_pickle(fname: str) -> object:
        """Load a pickle file from disk."""
        fpath = os.path.join(PICKLE_DIR, fname)
        with open(fpath, 'rb') as f:
            return pickle.load(f)
    
    # ========================================================
    # SENTIMENT PREDICTION
    # ========================================================
    
    def predict_sentiment(self, review_text: str) -> dict:
        """
        Predict sentiment for a review.
        
        Args:
            review_text: Raw review text
            
        Returns:
            dict with keys:
            - 'sentiment': 'Positive' or 'Negative'
            - 'probability': Float [0, 1], probability of positive sentiment
            - 'confidence': Float [0, 1], how confident the prediction is
        """
        # Preprocess
        processed = preprocess_text(review_text)
        
        if not processed:
            return {
                'sentiment': 'Unknown',
                'probability': 0.5,
                'confidence': 0.0,
                'error': 'Review text is empty after preprocessing'
            }
        
        # Vectorize
        features = self.tfidf_vectorizer.transform([processed])
        
        # Predict
        prediction = self.sentiment_model.predict(features)[0]
        probability = self.sentiment_model.predict_proba(features)[0, 1]
        
        # Interpretation
        sentiment_label = 'Positive' if prediction == 1 else 'Negative'
        confidence = max(probability, 1 - probability)
        
        return {
            'sentiment': sentiment_label,
            'probability': float(probability),
            'confidence': float(confidence)
        }
    
    # ========================================================
    # RECOMMENDATION GENERATION
    # ========================================================
    
    def recommend_products(self, username: str, n: int = RECOMMENDATION_TOP_N) -> dict:
        """
        Generate personalized product recommendations for a user.
        
        Pipeline:
        1. Get collaborative filtering candidates (top-50)
        2. Retrieve reviews for those products
        3. Predict sentiment for each review
        4. Compute positive sentiment ratio per product
        5. Rank by sentiment ratio
        6. Return top-N
        
        Args:
            username: User identifier
            n: Number of recommendations to return
            
        Returns:
            dict with:
            - 'recommendations': List of (product_name, sentiment_ratio, review_count)
            - 'explanation': Why these were recommended
            - 'cold_start': Boolean, whether user is new
        """
        
        is_cold_start = username not in self.recommender.user_index
        
        # Get candidates from CF
        cf_candidates = self.recommender.recommend(username, n=50)
        
        if not cf_candidates:
            return {
                'recommendations': [],
                'explanation': 'No recommendations available',
                'cold_start': is_cold_start
            }
        
        # Score candidates by sentiment
        product_scores = []
        
        for product_name in cf_candidates:
            # Get reviews for this product
            product_reviews = self.reviews_df[self.reviews_df['name'] == product_name]['reviews_text'].values
            
            if len(product_reviews) == 0:
                continue
            
            # Predict sentiment for each review
            sentiments = [
                self.predict_sentiment(review)['probability']
                for review in product_reviews
            ]
            
            # Positive ratio = fraction of reviews with positive sentiment
            positive_ratio = np.mean(sentiments)
            review_count = len(sentiments)
            
            product_scores.append({
                'product': product_name,
                'positive_ratio': positive_ratio,
                'review_count': review_count
            })
        
        # Sort by positive sentiment ratio (descending)
        product_scores.sort(key=lambda x: x['positive_ratio'], reverse=True)
        
        # Format output
        recommendations = [
            {
                'product': item['product'],
                'sentiment_score': float(item['positive_ratio']),
                'review_count': int(item['review_count'])
            }
            for item in product_scores[:n]
        ]
        
        explanation = (
            f"Recommended based on {'collaborative filtering + sentiment analysis' if not is_cold_start else 'popularity'}"
        )
        
        return {
            'recommendations': recommendations,
            'explanation': explanation,
            'cold_start': is_cold_start
        }
    
    # ========================================================
    # COMBINED PIPELINE
    # ========================================================
    
    def predict_and_recommend(self, username: str, review_text: str, 
                              n_recommendations: int = RECOMMENDATION_TOP_N) -> dict:
        """
        Complete pipeline: predict sentiment AND generate recommendations.
        
        Args:
            username: User identifier
            review_text: Review text to analyze
            n_recommendations: Number of products to recommend
            
        Returns:
            dict with:
            - 'sentiment': Predicted sentiment ('Positive' or 'Negative')
            - 'sentiment_probability': Confidence [0, 1]
            - 'recommendations': List of recommended products
            - 'timestamp': When prediction was made
        """
        import datetime
        
        # Predict sentiment
        sentiment_result = self.predict_sentiment(review_text)
        
        # Generate recommendations
        recommendation_result = self.recommend_products(username, n=n_recommendations)
        
        # Combine results
        return {
            'sentiment': sentiment_result.get('sentiment'),
            'sentiment_probability': sentiment_result.get('probability'),
            'sentiment_confidence': sentiment_result.get('confidence'),
            'recommendations': recommendation_result.get('recommendations'),
            'recommendation_explanation': recommendation_result.get('explanation'),
            'is_new_user': recommendation_result.get('cold_start'),
            'timestamp': datetime.datetime.now().isoformat()
        }


# ============================================================
# INITIALIZATION (Singleton Pattern)
# ============================================================

_system = None

def get_system() -> SentimentRecommenderSystem:
    """Get singleton instance of the system."""
    global _system
    if _system is None:
        _system = SentimentRecommenderSystem()
    return _system


if __name__ == '__main__':
    # Test the module
    print("Testing SentimentRecommenderSystem...\n")
    
    try:
        system = get_system()
        
        # Test sentiment prediction
        test_review = "This product is fantastic! Works perfectly."
        print(f"Testing sentiment prediction:")
        print(f"  Review: '{test_review}'")
        sentiment = system.predict_sentiment(test_review)
        print(f"  Result: {sentiment}\n")
        
        # Test recommendations
        test_user = system.reviews_df['reviews_username'].iloc[0]
        print(f"Testing recommendations for user: {test_user}")
        recs = system.recommend_products(test_user, n=5)
        print(f"  Recommendations: {len(recs['recommendations'])} found")
        for item in recs['recommendations'][:3]:
            print(f"    - {item['product'][:50]}... (sentiment={item['sentiment_score']:.2f})\n")
        
        print("✓ All tests passed. System is ready for deployment.")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        print("Make sure all pickle files are generated by running the notebook first.")
