"""
ML Utilities for Job Market Intelligence
Includes: Skill Analysis, AI Risk Assessment, Trend Forecasting
"""

import pandas as pd
import numpy as np
import ast
from collections import Counter
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
import warnings
warnings.filterwarnings('ignore')

class SkillAnalyzer:
    """Extract and analyze skills from job postings"""
    
    def __init__(self, jobs_df):
        self.jobs_df = jobs_df
        self.all_skills = self._extract_all_skills()
    
    def _extract_all_skills(self):
        """Extract all unique skills from dataset"""
        all_skills = set()
        for skill_str in self.jobs_df['skills'].dropna():
            try:
                if isinstance(skill_str, str):
                    skills = ast.literal_eval(skill_str)
                    all_skills.update(skills)
            except:
                pass
        return list(all_skills)
    
    def get_skills_for_role(self, role_name):
        """Get top skills required for a specific role"""
        role_jobs = self.jobs_df[self.jobs_df['role'].str.lower() == role_name.lower()]
        skill_freq = Counter()
        
        for skill_str in role_jobs['skills'].dropna():
            try:
                if isinstance(skill_str, str):
                    skills = ast.literal_eval(skill_str)
                    skill_freq.update(skills)
            except:
                pass
        
        return skill_freq.most_common(15)
    
    def get_emerging_skills(self, role_name):
        """Get emerging skills for a role"""
        role_jobs = self.jobs_df[self.jobs_df['role'].str.lower() == role_name.lower()]
        emerging = set()
        
        for emerging_str in role_jobs['emerging_skills'].dropna():
            try:
                if isinstance(emerging_str, str):
                    skills = ast.literal_eval(emerging_str)
                    emerging.update(skills)
            except:
                pass
        
        return list(emerging)[:10]
    
    def skill_importance_score(self, role_name):
        """Calculate importance of each skill for a role"""
        role_jobs = self.jobs_df[self.jobs_df['role'].str.lower() == role_name.lower()]
        total_jobs = len(role_jobs)
        
        skill_importance = {}
        for skill_str in role_jobs['skills'].dropna():
            try:
                if isinstance(skill_str, str):
                    skills = ast.literal_eval(skill_str)
                    for skill in skills:
                        if skill not in skill_importance:
                            skill_importance[skill] = 0
                        skill_importance[skill] += 1
            except:
                pass
        
        # Convert to percentage
        skill_importance = {
            skill: (count / total_jobs * 100) 
            for skill, count in skill_importance.items()
        }
        
        return dict(sorted(skill_importance.items(), key=lambda x: x[1], reverse=True)[:10])


class AIRiskAssessment:
    """Assess job automation/AI replacement risk"""
    
    def __init__(self, jobs_df):
        self.jobs_df = jobs_df
    
    def get_risk_for_role(self, role_name):
        """Get AI risk distribution for a role"""
        role_jobs = self.jobs_df[self.jobs_df['role'].str.lower() == role_name.lower()]
        
        risk_dist = {
            'Safe': 0,
            'Moderate': 0,
            'High Risk': 0
        }
        
        for risk in role_jobs['ai_risk'].dropna():
            if risk in risk_dist:
                risk_dist[risk] += 1
        
        total = sum(risk_dist.values())
        if total > 0:
            risk_dist = {k: (v/total)*100 for k, v in risk_dist.items()}
        
        return risk_dist
    
    def calculate_risk_score(self, role_name):
        """Calculate single risk score (0-100)"""
        risk_dist = self.get_risk_for_role(role_name)
        # Higher score = higher automation risk
        score = (risk_dist.get('High Risk', 0) * 1 + 
                risk_dist.get('Moderate', 0) * 0.5 + 
                risk_dist.get('Safe', 0) * 0)
        return min(100, score)
    
    def get_risky_jobs(self, threshold=70):
        """Get jobs with high automation risk"""
        risky = self.jobs_df[
            (self.jobs_df['ai_risk'] == 'High Risk') |
            ((self.jobs_df['ai_risk'] == 'Moderate') & 
             (self.jobs_df['growth_rate'] < 0.5))
        ]
        return risky[['role', 'job_title', 'ai_risk', 'growth_rate']].drop_duplicates()
    
    def get_safe_jobs(self):
        """Get jobs safe from automation"""
        safe = self.jobs_df[self.jobs_df['ai_risk'] == 'Safe']
        return safe[['role', 'job_title', 'ai_risk']].drop_duplicates()


class TrendForecaster:
    """Forecast future job trends and emerging roles"""
    
    def __init__(self, jobs_df, trend_df):
        self.jobs_df = jobs_df
        self.trend_df = trend_df
    
    def get_demand_trend(self, role_name):
        """Get demand trend for a role"""
        try:
            trend_data = self.trend_df[
                self.trend_df['role'].str.lower() == role_name.lower()
            ].sort_values('posted_date')
            
            if len(trend_data) > 0:
                return trend_data[['posted_date', 'job_count']].values.tolist()
            return []
        except:
            return []
    
    def predict_emerging_roles(self, top_n=5):
        """Predict emerging roles based on growth trends"""
        role_summary = self.jobs_df.groupby('role').agg({
            'job_count_per_role': 'first',
            'growth_rate': 'first',
            'skill_frequency': 'first'
        }).reset_index()
        
        # Sort by growth rate
        top_growing = role_summary.nlargest(top_n, 'growth_rate')
        
        return top_growing[['role', 'job_count_per_role', 'growth_rate']].to_dict('records')
    
    def get_skill_combinations(self):
        """Find trending skill combinations for new roles"""
        combinations = {}
        
        for skills_str, role in zip(self.jobs_df['skills'], self.jobs_df['role']):
            try:
                if isinstance(skills_str, str):
                    skills = sorted(ast.literal_eval(skills_str)[:3])
                    key = ' + '.join(skills)
                    if key not in combinations:
                        combinations[key] = []
                    combinations[key].append(role)
            except:
                pass
        
        # Find most common combinations
        trending = sorted(
            [(k, len(set(v))) for k, v in combinations.items()],
            key=lambda x: x[1],
            reverse=True
        )[:10]
        
        return trending


class CourseRecommender:
    """Recommend learning resources for skills"""
    
    COURSE_RESOURCES = {
        'python': [
            {'name': 'Python for Everybody', 'platform': 'Coursera', 'level': 'Beginner', 'link': 'coursera.org'},
            {'name': 'Complete Python Course', 'platform': 'Udemy', 'level': 'Intermediate', 'link': 'udemy.com'},
        ],
        'machine learning': [
            {'name': 'ML by Andrew Ng', 'platform': 'Coursera', 'level': 'Beginner', 'link': 'coursera.org'},
            {'name': 'Fast.ai ML Course', 'platform': 'Fast.ai', 'level': 'Intermediate', 'link': 'fast.ai'},
        ],
        'data science': [
            {'name': 'Data Science Specialization', 'platform': 'Coursera', 'level': 'Intermediate', 'link': 'coursera.org'},
            {'name': 'DS with Python', 'platform': 'DataCamp', 'level': 'Beginner', 'link': 'datacamp.com'},
        ],
        'sql': [
            {'name': 'SQL for Data Analysis', 'platform': 'Mode Analytics', 'level': 'Beginner', 'link': 'mode.com'},
            {'name': 'Advanced SQL', 'platform': 'DataCamp', 'level': 'Intermediate', 'link': 'datacamp.com'},
        ],
        'deep learning': [
            {'name': 'Deep Learning Specialization', 'platform': 'Coursera', 'level': 'Advanced', 'link': 'coursera.org'},
            {'name': 'Fast.ai DL Course', 'platform': 'Fast.ai', 'level': 'Intermediate', 'link': 'fast.ai'},
        ],
        'aws': [
            {'name': 'AWS Solutions Architect', 'platform': 'A Cloud Guru', 'level': 'Intermediate', 'link': 'acloudguru.com'},
            {'name': 'AWS Certified Developer', 'platform': 'Udemy', 'level': 'Intermediate', 'link': 'udemy.com'},
        ],
        'generative ai': [
            {'name': 'GenAI with LLMs', 'platform': 'DeepLearning.AI', 'level': 'Intermediate', 'link': 'deeplearning.ai'},
            {'name': 'LangChain for LLMs', 'platform': 'Udemy', 'level': 'Intermediate', 'link': 'udemy.com'},
        ],
    }
    
    @classmethod
    def recommend_courses(cls, skill_name):
        """Get course recommendations for a skill"""
        skill_lower = skill_name.lower()
        
        # Direct match
        if skill_lower in cls.COURSE_RESOURCES:
            return cls.COURSE_RESOURCES[skill_lower]
        
        # Partial match
        for key in cls.COURSE_RESOURCES.keys():
            if skill_lower in key or key in skill_lower:
                return cls.COURSE_RESOURCES[key]
        
        # Generic recommendations
        return [
            {'name': f'{skill_name} Fundamentals', 'platform': 'Coursera', 'level': 'Beginner', 'link': 'coursera.org'},
            {'name': f'Master {skill_name}', 'platform': 'Udemy', 'level': 'Intermediate', 'link': 'udemy.com'},
        ]
    
    @classmethod
    def get_learning_path(cls, current_skills, target_role_top_skills):
        """Create a learning path from current to target skills"""
        current_set = set(current_skills) if isinstance(current_skills, list) else set()
        target_set = set([s[0] for s in target_role_top_skills])
        
        skills_to_learn = target_set - current_set
        
        path = {
            'current': list(current_set),
            'to_learn': list(skills_to_learn),
            'target': list(target_set),
            'resources': {
                skill: cls.recommend_courses(skill)
                for skill in skills_to_learn
            }
        }
        
        return path
