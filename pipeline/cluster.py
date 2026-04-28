import numpy as np, uuid
from collections import defaultdict
from sklearn.cluster import AgglomerativeClustering
from pipeline.config import supabase

rows = supabase.table("photos").select("id,visual_embedding,dish,cuisine,category").eq("is_food", True).not_.is_("visual_embedding","null").execute().data
if not rows:
    print("no embeddings yet"); raise SystemExit
ids = [r["id"] for r in rows]
X = np.array([r["visual_embedding"] for r in rows], dtype=np.float32)
# normalize for cosine via euclidean
X = X / (np.linalg.norm(X, axis=1, keepdims=True)+1e-9)
labels = AgglomerativeClustering(n_clusters=None, distance_threshold=0.35, metric="euclidean", linkage="average").fit_predict(X)

groups = defaultdict(list)
for rid, lbl, r in zip(ids, labels, rows):
    groups[int(lbl)].append(r)

for lbl, items in groups.items():
    if len(items) < 2: continue
    dishes  = [i["dish"] for i in items if i.get("dish")]
    cuisines= [i["cuisine"] for i in items if i.get("cuisine")]
    cats    = [i["category"] for i in items if i.get("category")]
    label = max(set(dishes), key=dishes.count) if dishes else f"cluster_{lbl}"
    cid = str(uuid.uuid4())
    supabase.table("clusters").insert({
        "id": cid, "label": label,
        "cuisine": max(set(cuisines), key=cuisines.count) if cuisines else None,
        "category": max(set(cats), key=cats.count) if cats else None,
        "size": len(items),
        "hero_photo_id": items[0]["id"],
    }).execute()
    for it in items:
        supabase.table("photos").update({"cluster_id": cid}).eq("id", it["id"]).execute()
print("done clustering", len(groups), "groups")