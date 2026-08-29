-- tree_class_lookup.sql
UPDATE trees
SET tree_class = (
  SELECT tree_class 
  FROM cluster2class
  WHERE tree_cluster = soft_tree_class
)