
from app.quality_reviewer import quality_agent

sample_code = """
try:
    print(user["name"])
except:
    pass
"""

result = quality_agent(sample_code)

print("QUALITY AGENT TEST")
print("==================")
print(result)
