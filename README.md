# bigdataminingproject
Repo for both the BIG DATA and DATA MINING projects.

### Project structure

- **[project-name*]**: contains all the script files
  - **backup**: contains older versions of the scripts
- **data**: useful datasets for testing purpouse
- **tests**: output test files for all the algorithms implemented
- **res**: useful resources such as the road map and other stuff

*to be decided

--

### Algorithm 1: User-based collaborative filtering

Description description description

####* [usage]:

```python collaborative_filtering.py [user id] [k] [n]```, where:

* **user id**: the (uppercase) alphanumeric user ID
* **k**: the number of nearest neighbors to take into account
* **n**: the maximum number of recommendations to make

####* [sample output]:

```
List of recommendations in descending order:

('B0000ZFHJY', 1.6783058754304387)
('B00079UM2A', 1.6783058754304387)
('B0000867GG', 1.3803117380153767)
```

--

### Algorithm 2: Hierarchical clustering for detecting community structures

Description description description

####* [usage]:

```python script.py [param1] [param2] [paramN]```, where:

* **param1**: description
* **param2**: description
* **paramN**: description

####* [sample output]:

```
List of recommendations in descending order:

('B0000ZFHJY', 1.6783058754304387)
('B00079UM2A', 1.6783058754304387)
('B0000867GG', 1.3803117380153767)
```

--

### Algorithm 3: Dimensionality reduction by stemming, tokenization, TF-IDF

Description description description

####* [usage]:

```python main.py [threshold] [text]```, where:

* **threshold**: the (optional) IDF threshold used to compute the TF-IDF
* **text**: a possible search text to use

*if you want to input a product ID to get suggestions, insert only the threshold

####* [sample output]:

```
List of recommendations in descending order:

('B0000ZFHJY', 1.6783058754304387)
('B00079UM2A', 1.6783058754304387)
('B0000867GG', 1.3803117380153767)
```
