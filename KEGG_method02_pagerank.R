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

# Download the KGML file

# Assign random scores to each node for illustration
set.seed(42)
V(igraph_kegg)$score <- runif(vcount(igraph_kegg), min = 1, max = 10)  # Random scores for nodes

# Extract KEGG IDs (node names in the igraph object)
kegg_ids <- V(igraph_kegg)$name

# Convert KEGG IDs to Entrez Gene IDs
gene_ids <- translateKEGGID2GeneID(kegg_ids)

# Map Entrez Gene IDs to gene symbols
nodesNames <- sapply(mget(gene_ids, org.Hs.egSYMBOL, ifnotfound = NA), "[[", 1)
names(nodesNames) <- kegg_ids

# Update node labels in igraph with gene symbols (where available)
V(igraph_kegg)$label <- ifelse(!is.na(nodesNames), nodesNames, kegg_ids)

# PageRank Calculation
pr <- page.rank(igraph_kegg)$vector
V(igraph_kegg)$pagerank <- pr

# Display top 5 nodes by PageRank
top_nodes <- order(V(igraph_kegg)$pagerank, decreasing = TRUE)[1:5]
cat("Top 5 nodes by PageRank:\n")
for (i in 1:5) {
  cat("Node:", V(igraph_kegg)[top_nodes[i]]$label, "| PageRank Score:", V(igraph_kegg)[top_nodes[i]]$pagerank, "\n")
}

# Visualization
plot_color <- colorRampPalette(brewer.pal(9, "Blues"))(10)
V(igraph_kegg)$color <- plot_color[as.numeric(cut(V(igraph_kegg)$pagerank, breaks = 10))]
V(igraph_kegg)$size <- 10 + (V(igraph_kegg)$pagerank * 100)  # Node size based on PageRank

# Highlight top nodes with a border
V(igraph_kegg)$frame.color <- ifelse(V(igraph_kegg)$name %in% V(igraph_kegg)[top_nodes]$name, "red", "black")

# Plot with customized settings
plot(
  igraph_kegg, 
  vertex.label = V(igraph_kegg)$label, 
  vertex.size = V(igraph_kegg)$size,
  vertex.label.cex = 0.8,
  vertex.color = V(igraph_kegg)$color,
  vertex.frame.color = V(igraph_kegg)$frame.color,
  edge.width = 1,
  edge.color = "grey",
  main = "KEGG Pathway with Nodes Sized by PageRank Scores and Labeled with Gene Symbols"
)

