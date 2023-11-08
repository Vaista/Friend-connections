from dotenv import load_dotenv
import os


load_dotenv()


neo4j_user = os.environ.get('NEO4J_USER').strip()
neo4j_password = os.environ.get('NEO4J_PASSWORD').strip()
neo4j_host = os.environ.get('NEO4J_HOST').strip()
neo4j_port = os.environ.get('NEO4J_PORT').strip()


DATABASE_URL = f'bolt://{neo4j_user}:{neo4j_password}@{neo4j_host}:{neo4j_port}'
PROJECT_SECRET = os.environ.get('PROJECT_SECRET')
