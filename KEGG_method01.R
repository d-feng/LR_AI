library(KEGGgraph)
library(igraph)
require(pathview)
path_id <- "hsa04010"
#retrieveKGML(pathwayid = path_id, organism = "hsa", destfile = paste("tmp_dir/", path_id, ".xml"))
#test1_net <- parseKGML2Graph(file = paste0("./tmp_dir/", path_id, ".xml"), genesOnly = TRUE,,expandGenes=TRUE)
HIF1A_pathways <- c("hsa04066.xml", "hsa04137.xml", "hsa04140.xml",
                    
                    "hsa04659.xml", "hsa04919.xml", "hsa05167.xml",
                    "hsa05200.xml", "hsa05205.xml", "hsa05208.xml",
                    "hsa05211.xml", "hsa05230.xml", "hsa05231.xml",
                    "hsa05235.xml")

download.kegg(pathway.id = "04066", species = "hsa", kegg.dir = ".", file.type=c("xml", "png"))

#sfile <- system.file("extdata/hsa04010.xml",package="KEGGgraph")
sfile <- system.file("hsa04066.xml",package="KEGGgraph")
net=parseKGML2Graph(sfile,expandGenes=TRUE)

# Convert KEGGGraph object to igraph for easier manipulation
igraph_kegg <- igraph.from.graphNEL(net)

# Extract KEGG IDs (node names in the igraph object)
kegg_ids <- V(igraph_kegg)$name

# Convert KEGG IDs to Entrez Gene IDs
gene_ids <- translateKEGGID2GeneID(kegg_ids)

# Map Entrez Gene IDs to gene symbols
nodesNames <- sapply(mget(gene_ids, org.Hs.egSYMBOL, ifnotfound = NA), "[[", 1)
names(nodesNames) <- kegg_ids

# Update node labels in igraph with gene symbols (where available)
V(igraph_kegg)$label <- ifelse(!is.na(nodesNames), nodesNames, kegg_ids)


# Assign random scores to nodes (you'll likely have actual scores in real cases)
set.seed(42)
V(igraph_kegg)$score <- runif(vcount(igraph_kegg), min = 1, max = 10)  # Random scores for illustration

# Function to find paths and calculate path scores
find_high_score_paths <- function(graph, max_length = 3) {
  # Initialize an empty list to store path scores
  path_scores <- list()
  
  # Loop over all nodes to find paths of specified length
  for (node in V(graph)) {
    # Get paths of length up to max_length from the current node
    paths <- all_simple_paths(graph, from = node, mode = "out", cutoff = max_length)
    
    # Calculate score for each path and store
    for (path in paths) {
      path_score <- sum(V(graph)[path]$score)  # Sum of node scores in path
      path_scores[[length(path_scores) + 1]] <- list(
        path_nodes = path,
        path_score = path_score
      )
    }
  }
  
  # Sort paths by score in descending order
  path_scores <- path_scores[order(sapply(path_scores, function(x) x$path_score), decreasing = TRUE)]
  return(path_scores)
}

# Get the highest-score paths
high_score_paths <- find_high_score_paths(igraph_kegg, max_length = 3)

# Display the top 5 highest-score paths
for (i in 1:5) {
  cat("Path", i, ": Nodes =", V(igraph_kegg)[high_score_paths[[i]]$path_nodes]$label,
      "| Score =", high_score_paths[[i]]$path_score, "\n")
}


#################
plot_color <- colorRampPalette(brewer.pal(9, "Blues"))(10)
V(igraph_kegg)$color <- plot_color[as.numeric(cut(V(igraph_kegg)$score, breaks = 10))]

# Highlight top paths with a thicker edge width and different color
E(igraph_kegg)$width <- 1
E(igraph_kegg)$color <- "grey"



# Plot with customized settings
plot(
  igraph_kegg, 
  vertex.label = V(igraph_kegg)$name, 
  vertex.size = 10,
  vertex.label.cex = 0.8,
  vertex.color = V(igraph_kegg)$color,
  edge.width = E(igraph_kegg)$width,
  edge.color = E(igraph_kegg)$color,
  main = "KEGG Pathway with Top 5 Highest-Score Paths Highlighted"
)


## top 5 highest score
for (i in 1:5) {
  path <- high_score_paths[[i]]$path_nodes
  for (j in 1:(length(path) - 1)) {
    edge_id <- get_edge_ids(igraph_kegg, c(path[j], path[j + 1]))
    if (edge_id > 0) {
      E(igraph_kegg)[edge_id]$width <- 3
      E(igraph_kegg)[edge_id]$color <- "red"
    }
  }
}

# Plot with customized settings
plot(
  igraph_kegg, 
  #vertex.label = V(igraph_kegg)$name,
  vertex.label = V(igraph_kegg)$label,  # Use gene symbols as labels
  vertex.size = 10,
  vertex.label.cex = 0.8,
  vertex.color = V(igraph_kegg)$color,
  edge.width = E(igraph_kegg)$width,
  edge.color = E(igraph_kegg)$color,
  main = "KEGG Pathway with Top 5 Highest-Score Paths Highlighted"
)

library(igraph)
library(jsonlite)

# Example: assuming igraph_kegg is your igraph object
# Convert the igraph object into a JSON format



# Load necessary libraries
library(igraph)

# Assuming 'igraph_kegg' is your igraph object

# Extract node and edge data, converting IDs to character


# Create a mapping of internal igraph vertex IDs to KEGG IDs
vertex_ids <- as.character(V(igraph_kegg))  # Internal vertex IDs as character
kegg_ids <- V(igraph_kegg)$name             # KEGG IDs

# Map internal IDs to KEGG IDs using a named vector
vertex_to_kegg <- setNames(kegg_ids, vertex_ids)

# Convert internal vertex IDs in edges to KEGG IDs
edges$from <- vertex_to_kegg[as.character(edges$from)]
edges$to <- vertex_to_kegg[as.character(edges$to)]

# Check for any missing node references in edges
missing_from_nodes <- edges$from[!edges$from %in% unique_node_ids]
missing_to_nodes <- edges$to[!edges$to %in% unique_node_ids]

if (length(missing_from_nodes) == 0 && length(missing_to_nodes) == 0) {
  # All edges are valid; proceed with export
  graph_data <- list(nodes = nodes, edges = edges)
  write_json(graph_data, "graph_data.json")
  cat("Exported graph data to JSON.\n")
} else {
  cat("Missing 'from' node IDs in edges:", unique(missing_from_nodes), "\n")
  cat("Missing 'to' node IDs in edges:", unique(missing_to_nodes), "\n")
}














nodes <- data.frame(
  id = as.character(V(igraph_kegg)$name),  # Convert node IDs to character for consistency
  label = V(igraph_kegg)$label,
  score = V(igraph_kegg)$score
)

edges <- data.frame(
  from = as.character(head_of(igraph_kegg, E(igraph_kegg))),
  to = as.character(tail_of(igraph_kegg, E(igraph_kegg))),
  width = E(igraph_kegg)$width,
  color = E(igraph_kegg)$color
)



graph_data <- list(
  nodes = data.frame(
    id = V(igraph_kegg)$name,
    label = V(igraph_kegg)$label,
    score = V(igraph_kegg)$score
  ),
  edges = data.frame(
    from = as.character(head_of(igraph_kegg, E(igraph_kegg))),
    to = as.character(tail_of(igraph_kegg, E(igraph_kegg))),
    width = E(igraph_kegg)$width,
    color = E(igraph_kegg)$color
  )
)

# Export to JSON
write_json(graph_data, "graph_data.json")


# Assuming 'igraph_kegg' is your graph object




