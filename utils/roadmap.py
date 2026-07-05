class CareerRoadmap:

    _RESOURCES = {
        # Core Languages
        "python":           {"duration": "2 Weeks",  "task": "Complete Python Fundamentals and Build 3 Mini Projects"},
        "java":             {"duration": "3 Weeks",  "task": "Learn Core Java and Build Library Management System"},
        "c++":              {"duration": "2 Weeks",  "task": "Master OOP Concepts and DSA Problems"},
        "c#":               {"duration": "3 Weeks",  "task": "Learn C# and Build a .NET Console Application"},
        "typescript":       {"duration": "2 Weeks",  "task": "Add Types to a JavaScript Project and Build REST API"},
        "go":               {"duration": "3 Weeks",  "task": "Build a Concurrent CLI Tool in Go"},
        "golang":           {"duration": "3 Weeks",  "task": "Build a Concurrent CLI Tool in Go"},
        "rust":             {"duration": "4 Weeks",  "task": "Build a Systems Programming Project in Rust"},
        "scala":            {"duration": "3 Weeks",  "task": "Implement Functional Programming Patterns in Scala"},
        "kotlin":           {"duration": "2 Weeks",  "task": "Build an Android App with Kotlin"},
        "r":                {"duration": "2 Weeks",  "task": "Perform Statistical Analysis and Visualization in R"},
        # Databases
        "sql":              {"duration": "1 Week",   "task": "Practice SQL Queries and Database Design"},
        "mysql":            {"duration": "1 Week",   "task": "Design and Manage Relational Databases"},
        "postgresql":       {"duration": "1 Week",   "task": "Build a CRUD App with PostgreSQL and Python"},
        "mongodb":          {"duration": "1 Week",   "task": "Develop NoSQL CRUD Applications"},
        "redis":            {"duration": "4 Days",   "task": "Add Redis Caching to an Existing Flask/Django App"},
        "elasticsearch":    {"duration": "1 Week",   "task": "Build a Full-Text Search Feature with Elasticsearch"},
        "firebase":         {"duration": "1 Week",   "task": "Build a Real-Time Chat App with Firebase"},
        # Frontend
        "html":             {"duration": "4 Days",   "task": "Build Responsive Portfolio Website"},
        "css":              {"duration": "1 Week",   "task": "Create Modern Responsive UI"},
        "javascript":       {"duration": "2 Weeks",  "task": "Develop Interactive Web Applications"},
        "bootstrap":        {"duration": "3 Days",   "task": "Build Responsive Dashboard"},
        "tailwind":         {"duration": "4 Days",   "task": "Rebuild a UI Component Library with Tailwind CSS"},
        "react":            {"duration": "3 Weeks",  "task": "Develop Complete React Projects"},
        "angular":          {"duration": "3 Weeks",  "task": "Build an Angular CRUD Application"},
        "vue":              {"duration": "2 Weeks",  "task": "Develop a Vue.js SPA"},
        "next.js":          {"duration": "2 Weeks",  "task": "Build a Full-Stack Next.js App with SSR"},
        "svelte":           {"duration": "2 Weeks",  "task": "Build a Fast, Reactive UI with Svelte"},
        # Backend
        "node.js":          {"duration": "2 Weeks",  "task": "Develop REST APIs using Express"},
        "express":          {"duration": "1 Week",   "task": "Build Backend Services"},
        "flask":            {"duration": "1 Week",   "task": "Develop Flask CRUD Application"},
        "django":           {"duration": "2 Weeks",  "task": "Develop Student Management System"},
        "fastapi":          {"duration": "1 Week",   "task": "Build a High-Performance REST API with FastAPI"},
        "graphql":          {"duration": "1 Week",   "task": "Replace a REST API with a GraphQL Schema"},
        # ML / AI
        "machine learning": {"duration": "4 Weeks",  "task": "Build ML Prediction Models"},
        "deep learning":    {"duration": "4 Weeks",  "task": "Implement CNN and RNN Models"},
        "tensorflow":       {"duration": "2 Weeks",  "task": "Develop Image Classification Project"},
        "keras":            {"duration": "1 Week",   "task": "Build Neural Networks"},
        "pytorch":          {"duration": "2 Weeks",  "task": "Train Deep Learning Models"},
        "opencv":           {"duration": "2 Weeks",  "task": "Build Computer Vision Project"},
        "scikit-learn":     {"duration": "1 Week",   "task": "Train and Evaluate 5 Classification Models"},
        "xgboost":          {"duration": "1 Week",   "task": "Win a Kaggle Competition using XGBoost"},
        "lightgbm":         {"duration": "1 Week",   "task": "Build a Gradient Boosting Pipeline"},
        "hugging face":     {"duration": "2 Weeks",  "task": "Fine-Tune a Pre-trained Transformer on Custom Data"},
        "transformers":     {"duration": "2 Weeks",  "task": "Fine-Tune a BERT/GPT Model for NLP Task"},
        "langchain":        {"duration": "2 Weeks",  "task": "Build a RAG-based Q&A Chatbot with LangChain"},
        "generative ai":    {"duration": "3 Weeks",  "task": "Build a GenAI App using LLM APIs"},
        "llm":              {"duration": "3 Weeks",  "task": "Deploy and Prompt-Engineer an Open-Source LLM"},
        "mlflow":           {"duration": "1 Week",   "task": "Track ML Experiments with MLflow"},
        "nlp":              {"duration": "2 Weeks",  "task": "Build Resume Parser and Chatbot"},
        "computer vision":  {"duration": "2 Weeks",  "task": "Implement Object Detection Project"},
        # Data Engineering
        "pandas":           {"duration": "1 Week",   "task": "Complete Data Wrangling Project with Pandas"},
        "numpy":            {"duration": "4 Days",   "task": "Implement Linear Algebra Operations with NumPy"},
        "apache spark":     {"duration": "2 Weeks",  "task": "Process 1M+ Row Dataset using PySpark"},
        "kafka":            {"duration": "2 Weeks",  "task": "Build a Real-Time Event Streaming Pipeline"},
        "airflow":          {"duration": "1 Week",   "task": "Automate an ETL Pipeline with Apache Airflow"},
        "dbt":              {"duration": "1 Week",   "task": "Build a Data Transformation Pipeline with dbt"},
        # DevOps / Cloud
        "docker":           {"duration": "1 Week",   "task": "Containerize Flask Application"},
        "kubernetes":       {"duration": "2 Weeks",  "task": "Deploy Applications using Kubernetes"},
        "terraform":        {"duration": "2 Weeks",  "task": "Provision Cloud Infrastructure as Code"},
        "jenkins":          {"duration": "1 Week",   "task": "Set Up a CI/CD Pipeline with Jenkins"},
        "ci/cd":            {"duration": "1 Week",   "task": "Build GitHub Actions CI/CD Pipeline"},
        "aws":              {"duration": "2 Weeks",  "task": "Deploy Cloud Applications"},
        "azure":            {"duration": "2 Weeks",  "task": "Learn Azure Cloud Services"},
        "gcp":              {"duration": "2 Weeks",  "task": "Deploy a GCP Cloud Run Application"},
        "linux":            {"duration": "1 Week",   "task": "Complete Linux Command Line and Bash Scripting"},
        "bash":             {"duration": "4 Days",   "task": "Write Shell Scripts to Automate System Tasks"},
        "git":              {"duration": "3 Days",   "task": "Master Git Version Control"},
        "github":           {"duration": "2 Days",   "task": "Publish and Maintain Projects"},
        # BI / Visualization
        "power bi":         {"duration": "1 Week",   "task": "Create Interactive Dashboards"},
        "tableau":          {"duration": "1 Week",   "task": "Develop Business Dashboards"},
        "streamlit":        {"duration": "4 Days",   "task": "Build and Deploy an ML Demo App with Streamlit"},
        "grafana":          {"duration": "4 Days",   "task": "Set Up Observability Dashboard with Grafana"},
        # Methodologies
        "agile":            {"duration": "3 Days",   "task": "Complete Agile/Scrum Fundamentals Certification"},
        "scrum":            {"duration": "3 Days",   "task": "Manage a Sprint and Run Retrospectives"},
    

        "sql":              {"duration": "1 Week",    "task": "Practice SQL Queries and Database Design"},
        "mysql":            {"duration": "1 Week",    "task": "Design and Manage Relational Databases"},
        "mongodb":          {"duration": "1 Week",    "task": "Develop NoSQL CRUD Applications"},
        "html":             {"duration": "4 Days",    "task": "Build Responsive Portfolio Website"},
        "css":              {"duration": "1 Week",    "task": "Create Modern Responsive UI"},
        "javascript":       {"duration": "2 Weeks",   "task": "Develop Interactive Web Applications"},
        "bootstrap":        {"duration": "3 Days",    "task": "Build Responsive Dashboard"},
        "react":            {"duration": "3 Weeks",   "task": "Develop Complete React Projects"},
        "node.js":          {"duration": "2 Weeks",   "task": "Develop REST APIs using Express"},
        "express":          {"duration": "1 Week",    "task": "Build Backend Services"},
        "flask":            {"duration": "1 Week",    "task": "Develop Flask CRUD Application"},
        "django":           {"duration": "2 Weeks",   "task": "Develop Student Management System"},
        "machine learning": {"duration": "4 Weeks",   "task": "Build ML Prediction Models"},
        "deep learning":    {"duration": "4 Weeks",   "task": "Implement CNN and RNN Models"},
        "tensorflow":       {"duration": "2 Weeks",   "task": "Develop Image Classification Project"},
        "keras":            {"duration": "1 Week",    "task": "Build Neural Networks"},
        "pytorch":          {"duration": "2 Weeks",   "task": "Train Deep Learning Models"},
        "opencv":           {"duration": "2 Weeks",   "task": "Build Computer Vision Project"},
        "docker":           {"duration": "1 Week",    "task": "Containerize Flask Application"},
        "kubernetes":       {"duration": "2 Weeks",   "task": "Deploy Applications using Kubernetes"},
        "aws":              {"duration": "2 Weeks",   "task": "Deploy Cloud Applications"},
        "azure":            {"duration": "2 Weeks",   "task": "Learn Azure Cloud Services"},
        "git":              {"duration": "3 Days",    "task": "Master Git Version Control"},
        "github":           {"duration": "2 Days",    "task": "Publish and Maintain Projects"},
        "power bi":         {"duration": "1 Week",    "task": "Create Interactive Dashboards"},
        "tableau":          {"duration": "1 Week",    "task": "Develop Business Dashboards"},
        "nlp":              {"duration": "2 Weeks",   "task": "Build Resume Parser and Chatbot"},
        "computer vision":  {"duration": "2 Weeks",   "task": "Implement Object Detection Project"},
    }

    def generate_roadmap(self, missing_skills):
        roadmap = []
        for skill in missing_skills:
            resource = self._RESOURCES.get(skill.lower())
            if resource:
                roadmap.append({"skill": skill, **resource})
            else:
                roadmap.append({"skill": skill, "duration": "Self Paced", "task": "Learn fundamentals and build one project."})
        return roadmap
