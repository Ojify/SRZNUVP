import os
import sys

# Добавляем корень проекта в sys.path, чтобы тесты видели модули
# domain_projects, domain_users, domain_applications, domain_statuses
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))