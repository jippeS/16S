args = commandArgs(trailingOnly=TRUE)
library(ggplot2)
# library(scales)
time_table<- read.csv(file = args[1], header = T, sep = "\t")
time_table <- time_table[order(time_table$s,decreasing=TRUE),]

colors <- c("#6FB000", "#00C08E", "#F863DF", "#00A7FF", "#E9842C", "#F8766D", "#00BDD4", "#FF6A9A", "#E26EF7", "#00BD61",
            "#D69100", "#7F96FF", "#9CA700", "#00B813", "#FF62BF", "#BC81FF", "#BC9D00", "#00C0B4", "#00B5EE", "#F8769D")

time_table$alpha <- 0
time_table$alpha[1:4] <- 1

# Convert 's' column to matrix with a single column
time_table$s <- matrix(time_table$s, ncol = 1)

# Calculate the total values for each category
time_table$total <- rowSums(time_table[, "s"])

# Reorder the levels in the 'name' column
time_table$name <- factor(time_table$name, levels = time_table$name)

# Get the number of unique categories
num_categories <- length(unique(time_table$name))

# Create the stacked barplot with standard color scheme
plot <- ggplot(time_table, aes(fill = name, y = s/60, x = 1)) +
  geom_bar(position = "stack", stat = "identity") +
  scale_fill_manual(values = colors) +  # Apply standard color scheme
  # Add labels within the biggest four parts
  geom_text(data = time_table, alpha = time_table$alpha,
            aes(label = paste0(name, ": ", round(s/60, 1), " min")), 
            position = position_stack(vjust = 0.5), size = 3) +
  labs(y = "Time (minutes)", x = "") +
  theme_minimal()

ggsave(args[2], plot, width = 8, height = 6, units = "in", dpi = 300)