# Ingredients API

A Django-based REST API that provides semantic search capabilities for ingredients with detailed allergen information. The service uses OpenAI embeddings and FAISS vector database to enable fuzzy matching and similarity search for ingredient queries.

## Disclaimer

**Note**: The actual ingredient names, details, and data files have been removed from this repository to preserve the intellectual property of the [Clearplate mobile app](https://www.clearplateapp.com/). This repository demonstrates the technical implementation and architecture of the semantic search system.

## Features

- **Semantic Search**: Find ingredients using natural language queries and fuzzy matching
- **Allergen Information**: Comprehensive allergen profiles for 9 major allergens (Egg, Fish, Milk, Peanut, Sesame, Shellfish, Soy, Tree Nut, Wheat)
- **Batch Processing**: Handle multiple ingredient queries in a single API call
- **Vector Database**: FAISS-powered similarity search for accurate ingredient matching
- **API Authentication**: Secure access with API key validation

## Architecture

The service consists of two main components:

1. **Embedding Generation** (`createEmbedding.js`): Node.js script that generates OpenAI embeddings for ingredient names using the `text-embedding-ada-002` model
2. **Search API** (`ingredients_repository.py`): Python module using LangChain and FAISS for vector similarity search

## API Endpoints

### POST `/ingredients/batch`

Retrieve allergen information for multiple ingredients using semantic search.

**Headers:**
- `X-Api-Key`: Required API key for authentication
- `Content-Type`: application/json

**Request Body:**
```json
{
  "ingredient_queries": ["tomato", "wheat flour", "peanut butter"],
  "num_results": 3
}
```

**Response:**
```json
{
  "tomato": [
    {
      "name": "Tomato",
      "category": "Vegetable",
      "description": "Fresh tomato",
      "allergen_profile": {
        "321705f7d2784acd9e8b44b8436b9356": {
          "allergen": {"id": "321705f7d2784acd9e8b44b8436b9356", "name": "Egg"},
          "rating": "0",
          "note": "No egg content"
        }
        // ... other allergen profiles
      },
      "relevancy_score": 0.95
    }
  ]
}
```

## Setup and Installation

### Prerequisites

- Python 3.8+
- Node.js (for embedding generation)
- OpenAI API key

### Environment Variables

```bash
OPENAI_API_KEY=your_openai_api_key
ALLERGY_INSIGHTS_KEY=your_api_key_for_authentication
```

### Installation

1. Install Python dependencies:
```bash
pip install -r requirements.txt
```

2. Generate embeddings (if needed):
```bash
cd ingredients/
node createEmbedding.js
```

3. Run the Django server:
```bash
python manage.py runserver
```

### Docker Deployment

The service includes Docker configuration and AWS ECR deployment scripts:

```bash
# Build and push to ECR
./ecr_push.sh

# Run with user data script
./user_data.sh
```

## Dependencies

### Python
- Django 5.0.4
- LangChain with OpenAI integration
- FAISS for vector search
- simplejson for JSON handling

### Node.js
- Native HTTPS module for OpenAI API calls

## Data Structure

The service processes ingredient data with:
- **Ingredient Names**: Searchable ingredient database
- **Allergen Profiles**: Ratings and notes for 9 major allergens
- **Vector Embeddings**: OpenAI-generated embeddings for semantic search

## Performance

- Parallel processing for batch ingredient lookups
- In-memory FAISS vector database for fast similarity search
- Configurable result limits per query