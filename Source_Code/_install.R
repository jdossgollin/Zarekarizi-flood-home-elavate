package_check <- function(x) {
  if (!require(x, character.only = TRUE)) {
    install.packages(x, dependencies = TRUE)
    library(x, character.only = TRUE)
  }
}

package_list <- c(
    "DEoptim",
    "extRemes",
    "evd",
    "evdbayes",
    "evir",
    "fields",
    "ismev",
    "Kendall",
    "lhs",
    "plotrix",
    "pracma",
    "sensitivity",
    "truncnorm"
)

package.check <- lapply(
  package_list,
  package_check 
)
