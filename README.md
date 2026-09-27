# Genshin Impact and Zenless Zone Zero Analysis Tools

A collection of Python tools for analyzing different aspects of Genshin Impact using simulations, probability calculations, and player data.

The project currently includes:

- Artifact evaluation and upgrade probability analysis
- Artifact reroll and crafting analysis
- Wish / pull statistics analysis
- Player survey analysis
- Data visualization and statistical processing

## Artifact Analysis

Tools for evaluating character artifacts and estimating how difficult it is to obtain an equivalent or better artifact.

### Artifact Score

Each artifact is evaluated based on the character's preferred substats.

Instead of using a fixed universal artifact score, substat values are weighted individually for each character. The weights can take character base stats into account, including the relationship between flat and percentage-based stats.

Generated artifacts are used to estimate the probability of obtaining an artifact better than the currently equipped one.

The resulting score represents the rarity of the artifact relative to possible drops:

- Higher score means that obtaining an improvement is less likely.
- Scores close to 100 indicate artifacts that are difficult to replace.

Character score is calculated from the scores of all five equipped artifacts.

### Artifact Simulation

Large sets of random artifacts are generated according to the game's artifact generation rules.

The simulation includes:

- Main stat probabilities
- Weighted substat selection
- 3-stat and 4-stat starting artifacts
- 4 or 5 artifact upgrade rolls
- Four possible roll values for every substat
- Exclusion of the main stat from possible substats

Generated artifacts are stored in binary files for faster evaluation.

Each generated artifact stores only its four substats:

    (stat_id, roll_count, total_value) × 4

This reduces storage size and allows artifact scores to be calculated without processing unused stats.

## Artifact Reroll Analysis

The project can calculate the probability that rerolling an artifact produces a better result.

The original four substats and their initial rolls are preserved, while upgrade rolls are regenerated.

The calculation supports guarantees requiring at least:

- 2 upgrade rolls into two selected substats
- 3 upgrade rolls
- 4 upgrade rolls

The two guaranteed substats are automatically selected according to their value for the character.

Possible upgrade distributions and roll-value distributions are precomputed to make repeated calculations faster.

## Artifact Crafting Analysis

The project also estimates the probability of obtaining an improvement through artifact crafting.

For each artifact, the two most valuable available substats are selected.

Generated artifacts are filtered according to crafting requirements:

- Both selected substats must be present.
- The selected substats must contain at least four total rolls, including their initial rolls.

The resulting probability shows how often a crafted artifact satisfying these conditions would be better than the currently equipped artifact.

## Wish Analysis

The project contains tools for analyzing Genshin Impact wish history.

The analysis can be used to process pull data and calculate statistics such as:

- Number of pulls
- 5-star acquisition statistics
- Pity distributions
- Average pull counts
- Character and banner statistics
- Probability-related metrics

The collected data can also be aggregated and visualized to compare results between players or datasets.

## Survey Analysis

The project includes scripts for processing and analyzing player surveys.

Survey data can be grouped and transformed to study relationships between different responses.

The analysis includes:

- Response distributions
- Group comparisons
- Average values
- Percentage tables
- Relationships between player activity and survey answers
- Visualization of results

For example, survey results can be used to compare player ratings with the number of hours played or other player characteristics.

## Technologies

- Python
- NumPy
- Pandas
- Matplotlib
- JSON
- Binary data processing with `struct`

Jupyter Notebook is also used for exploratory analysis, testing, and visualization.

## Project Structure

The repository contains separate scripts and notebooks for different types of analysis.

Generated datasets, simulation files, and intermediate results are not intended to be stored in Git and can be recreated when necessary.

Large generated artifact datasets are stored locally in binary format to improve loading and evaluation performance.

## Performance

Artifact simulation and evaluation are designed to handle large generated datasets.

Several optimizations are used, including:

- Compact binary artifact representation
- Processing only four existing substats instead of full stat arrays
- Precomputed roll distributions
- Cached roll-value distributions
- Batch generation and binary writing

These optimizations significantly reduce the time required to evaluate artifacts across multiple characters.

## Status

The project is primarily intended for personal statistical analysis and experimentation.

Different parts of the project may use different datasets and assumptions as the analysis tools continue to evolve.
