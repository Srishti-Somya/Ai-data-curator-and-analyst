#!/usr/bin/env python3
"""
AI Tool for Data Curation and Analysis - Query Testing Script

This script provides an easy way to test different queries against the system.
"""

import requests
import json
import time
import sys
from typing import List, Tuple

def test_query(query: str, keywords: List[str], columns: List[str] = None) -> dict:
    """
    Test a single query against the system.
    
    Args:
        query: The search query
        keywords: List of keywords to search for
        columns: List of columns to save (default: Person, Org, Date, Loc)
    
    Returns:
        Response from the API
    """
    if columns is None:
        columns = ["Person", "Org", "Date", "Loc"]
    
    url = "http://127.0.0.1:8000/process"
    payload = {
        "query": query,
        "keywords": keywords,
        "columns_to_save": columns
    }
    
    try:
        print(f"🔍 Testing query: {query}")
        print(f"   Keywords: {keywords}")
        
        response = requests.post(url, json=payload, timeout=60)
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Success: {result.get('message', 'Processing completed')}")
            print(f"   CSV file: {result.get('csv_file', 'N/A')}")
            print(f"   SVG file: {result.get('svg_file', 'N/A')}")
            return result
        else:
            print(f"❌ Error: {response.status_code}")
            print(f"   Response: {response.text}")
            return None
            
    except requests.exceptions.ConnectionError:
        print("❌ Connection Error: Make sure both servers are running")
        print("   Run: ./quick_start.sh")
        return None
    except requests.exceptions.Timeout:
        print("❌ Timeout: Query took too long to process")
        return None
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return None
    finally:
        print("-" * 60)

def run_predefined_tests():
    """Run a set of predefined test queries."""
    
    # Predefined test queries
    test_queries = [
        {
            "name": "Climate Change Research",
            "query": "climate change solutions 2024",
            "keywords": ["renewable energy", "carbon capture"]
        },
        {
            "name": "Quantum Computing",
            "query": "quantum computing applications 2024",
            "keywords": ["quantum", "computing", "algorithms"]
        },
        {
            "name": "Space Exploration",
            "query": "space exploration missions 2024",
            "keywords": ["NASA", "Mars", "satellite"]
        },
        {
            "name": "AI and Machine Learning",
            "query": "artificial intelligence trends 2024",
            "keywords": ["machine learning", "AI development"]
        },
        {
            "name": "Cancer Research",
            "query": "cancer research breakthroughs 2024",
            "keywords": ["oncology", "treatment", "clinical trials"]
        },
        {
            "name": "Blockchain Technology",
            "query": "blockchain technology developments 2024",
            "keywords": ["cryptocurrency", "decentralized", "smart contracts"]
        }
    ]
    
    print("🧪 Running Predefined Test Queries")
    print("=" * 60)
    
    results = []
    for i, test in enumerate(test_queries, 1):
        print(f"\n{i}. {test['name']}")
        result = test_query(test['query'], test['keywords'])
        results.append({
            'name': test['name'],
            'success': result is not None,
            'result': result
        })
        time.sleep(2)  # Small delay between queries
    
    # Summary
    print("\n📊 Test Summary")
    print("=" * 60)
    successful = sum(1 for r in results if r['success'])
    total = len(results)
    print(f"Successful: {successful}/{total}")
    
    for result in results:
        status = "✅" if result['success'] else "❌"
        print(f"{status} {result['name']}")

def interactive_mode():
    """Run in interactive mode for custom queries."""
    
    print("🎯 Interactive Query Mode")
    print("=" * 60)
    print("Enter your queries (type 'quit' to exit)")
    print()
    
    while True:
        try:
            query = input("Enter search query: ").strip()
            if query.lower() in ['quit', 'exit', 'q']:
                break
            if not query:
                continue
                
            keywords_input = input("Enter keywords (comma-separated): ").strip()
            keywords = [k.strip() for k in keywords_input.split(',') if k.strip()]
            
            if not keywords:
                keywords = ["technology", "research"]
                print(f"Using default keywords: {keywords}")
            
            test_query(query, keywords)
            
        except KeyboardInterrupt:
            print("\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"❌ Error: {e}")

def main():
    """Main function."""
    
    print("🤖 AI Tool for Data Curation and Analysis - Query Tester")
    print("=" * 60)
    
    # Check if servers are running
    try:
        response = requests.get("http://127.0.0.1:8000/docs", timeout=5)
        print("✅ Main server is running")
    except:
        print("❌ Main server is not running")
        print("   Please start the servers first:")
        print("   ./quick_start.sh")
        return
    
    try:
        response = requests.get("http://127.0.0.1:8001/docs", timeout=5)
        print("✅ Scraping service is running")
    except:
        print("❌ Scraping service is not running")
        print("   Please start the servers first:")
        print("   ./quick_start.sh")
        return
    
    print()
    
    # Choose mode
    print("Choose testing mode:")
    print("1. Run predefined tests")
    print("2. Interactive mode")
    print("3. Single custom query")
    
    try:
        choice = input("\nEnter your choice (1-3): ").strip()
        
        if choice == "1":
            run_predefined_tests()
        elif choice == "2":
            interactive_mode()
        elif choice == "3":
            query = input("Enter search query: ").strip()
            keywords_input = input("Enter keywords (comma-separated): ").strip()
            keywords = [k.strip() for k in keywords_input.split(',') if k.strip()]
            test_query(query, keywords)
        else:
            print("Invalid choice. Running predefined tests...")
            run_predefined_tests()
            
    except KeyboardInterrupt:
        print("\n👋 Goodbye!")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    main() 