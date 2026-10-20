from pathlib import Path

#   folders  
baseDir = Path(__file__).resolve().parent.parent
appDir = baseDir / "app"
dataDir = baseDir / "data"
templatesDir = appDir / "templates"
staticDir = appDir / "static"

#   data files  
displayDataPath = dataDir / "display_data.csv"
preprocessedDataPath = dataDir / "Global_data_preprocessed.csv"
modelPath = dataDir / "model.pkl"

#   model settings  
featureColumns = ["environment_score", "social_score", "governance_score"]
targetColumn = "total_score"

# the raw model output is squeezed between these two numbers to get a 0-100 trust score
rawScoreMin = 600
rawScoreMax = 1536

# highest possible value for each pillar (used to draw the progress bars)
maxEnvironmentScore = 719
maxSocialScore = 667
maxGovernanceScore = 475

#   page settings  
defaultSector = "Technology"
topCompaniesLimit = 15

# these numbers are shown as plain text in the hero section and footer
heroDataPoints = 12
modelAccuracy = "96.6%"
