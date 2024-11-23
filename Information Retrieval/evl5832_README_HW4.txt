Ad Hoc Information Retrieval System

This project is an Ad Hoc Information Retrieval system using TF-IDF weights and cosine similarity scores. The system processes a set of queries and abstracts to generate TF-IDF vectors, computes cosine similarity scores between query and abstract vectors, and outputs the top 100 ranked abstracts for each query.

Input Files Provided:
    1. cran.all.1400: A collection of 1400 abstracts of aerodynamics journal articles
    2. cran.qry: A set of 225 queries with associated query IDs
    3. cranqrel: An answer key mapping queries to abstracts with relevance scores
    4. stop_list.py: A Python file containing a list of stop words to filter out during processing

Output:  
    - saved in the file "output.txt"
    - includes the top 100 abstracts for each query, sorted by cosine similarity score
    - Each line is in the format: 
        <query_id> <abstract_id> <cosine_similarity_score>

Run the program:
    python Information_Retrieval.py