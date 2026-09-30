import numpy as np

# Let's pretend our LLM gave us these 2D coordinates for three sentences:
# A: "I am planting rice"
# B: "Sowing paddy seeds"
# C: "I like driving fast cars"

vec_A = np.array([0.9, 0.1])
vec_B = np.array([0.8, 0.3])
vec_C = np.array([-0.2, 0.9])

def cosine_distance(v1, v2):
    # Cosine distance is 1 - Cosine Similarity
    dot_product = np.dot(v1, v2)
    norm_v1 = np.linalg.norm(v1)
    norm_v2 = np.linalg.norm(v2)
    similarity = dot_product / (norm_v1 * norm_v2)
    return 1 - similarity

print("Distance A to B (Rice to Paddy):", cosine_distance(vec_A, vec_B))
print("Distance A to C (Rice to Cars):", cosine_distance(vec_A, vec_C))
