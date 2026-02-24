# Sentiment-Based Product Recommendation System

An end-to-end machine learning system that combines collaborative filtering with NLP-powered sentiment analysis to deliver personalized product recommendations.

## 🎯 Project Overview

This capstone project addresses a critical limitation in traditional e-commerce recommender systems: they rely solely on numerical ratings while ignoring the rich sentiment signals in review text. Our hybrid system filters collaborative filtering candidates through sentiment analysis to surface products users genuinely praise.

### Business Context
- **Platform**: Ebuss e-commerce (competing with Amazon & Flipkart)
- **Scale**: 30,000+ reviews, 200+ products, 20,000+ users
- **Objective**: Reduce recommendation noise and improve customer trust

## 🏗️ System Architecture

```
User Input (username)
    ↓
Collaborative Filter → Top-20 candidate products
    ↓
Sentiment Model → Predict positive/negative per review
    ↓
Rank by positive sentiment ratio
    ↓
Top-5 Final Recommendations
```

## ✨ Key Features

- **Hybrid Recommendation**: Combines user-based CF with sentiment filtering
- **NLP Pipeline**: Advanced text preprocessing with lemmatization and bigrams
- **4-Model Comparison**: Logistic Regression, Naive Bayes, Linear SVC, Gradient Boosting
- **Production-Ready**: Pickled models with <5ms inference latency
- **Memory-Efficient**: Sparse matrix operations for 99.4% sparse user-item matrix

## 📊 Performance Metrics

| Model | CV F1 | Test F1 | AUC |
|-------|-------|---------|-----|
| Logistic Regression | 0.943 | 0.941 | 0.985 |
| Linear SVC | 0.940 | 0.938 | 0.983 |
| Multinomial NB | 0.925 | 0.923 | 0.978 |
| Gradient Boosting | 0.937 | 0.935 | 0.982 |

## 🚀 Getting Started

### Prerequisites

```bash
python >= 3.8
pandas
numpy
scikit-learn
nltk
matplotlib
seaborn
scipy
```

### Installation

```bash
# Clone the repository
git clone https://github.com/YOUR_USERNAME/sentiment-recommendation.git
cd sentiment-recommendation

# Install dependencies
pip install -r requirements.txt

# Download NLTK data
python -c "import nltk; nltk.download(['punkt', 'stopwords', 'wordnet', 'omw-1.4'])"
```

### Usage

1. **Train the models** (run the complete notebook):
   ```bash
   jupyter notebook sentiment_recommendation_notebook.ipynb
   ```

2. **Load pre-trained models**:
   ```python
   import pickle
   
   with open('pickle/sentiment_model.pkl', 'rb') as f:
       sentiment_model = pickle.load(f)
   
   with open('pickle/user_based_cf.pkl', 'rb') as f:
       recommender = pickle.load(f)
   ```

3. **Get recommendations**:
   ```python
   # Get top-20 candidates
   candidates = recommender.recommend(username='john_doe', n=20)
   
   # Filter by sentiment
   final_recommendations = sentiment_filter(
       candidates, 
       sentiment_model, 
       vectorizer, 
       reviews_df
   )
   ```

## 📁 Project Structure

```
sentiment-recommendation/
├── sentiment_recommendation_notebook.ipynb  # Main training pipeline
├── sample30.csv                             # Dataset (30k reviews)
├── pickle/                                  # Serialized models
│   ├── sentiment_model.pkl
│   ├── tfidf_vectorizer.pkl
│   ├── user_based_cf.pkl
│   └── master_reviews.pkl
├── eda_plots.png                           # Exploratory visualizations
├── confusion_matrices.png                  # Model evaluation
├── requirements.txt                        # Python dependencies
└── README.md                               # This file
```

## 🧪 Model Selection Rationale

### Sentiment Classifier: Logistic Regression
- ✅ Highest weighted F1 (0.941) and AUC (0.985)
- ✅ Calibrated probabilities for confidence-aware ranking
- ✅ Interpretable coefficients for business insights
- ✅ Sub-5ms inference latency

### Recommender: User-Based Collaborative Filtering
- ✅ Lower proxy RMSE vs item-based CF
- ✅ Personalized to individual user taste
- ✅ Robust cold-start fallback
- ✅ Mean-centered cosine similarity removes rating bias

## 🔬 Technical Highlights

1. **Advanced Text Preprocessing**
   - Lemmatization (vs crude stemming)
   - Bigram support for "not good", "highly recommend"
   - Negation-aware stopword removal
   - URL/email/number handling

2. **TF-IDF Tuning**
   - 50,000 features with sublinear scaling
   - Min_df=3, max_df=0.90 for noise filtering
   - Unigram + bigram extraction

3. **Sparse Matrix Operations**
   - CSR format for 99.4% sparse rating matrix
   - 100× memory reduction vs dense Pandas pivot
   - Cosine similarity on mean-centered ratings

4. **Hyperparameter Tuning**
   - GridSearchCV with stratified K-fold
   - Custom decision threshold (0.55) for precision-recall balance

##  Learning Outcomes

- End-to-end ML pipeline: data cleaning → EDA → feature engineering → modeling → deployment
- Hybrid recommender system design
- NLP for sentiment classification
- Production ML: serialization, inference optimization
- Business-aware model selection

##  Future Enhancements

- [ ] Matrix factorization (SVD/ALS) for better cold-start handling
- [ ] BERT fine-tuning for contextual sentiment
- [ ] Flask API for real-time inference
- [ ] A/B testing framework
- [ ] Explainable AI: LIME/SHAP for recommendation transparency

##  Author

Created as part of an industry-grade ML capstone project.

##  License

This project is available under the MIT License.

##  Acknowledgments

- Dataset: Ebuss e-commerce platform
- Inspiration: Hybrid recommendation systems in production at Amazon/Netflix
