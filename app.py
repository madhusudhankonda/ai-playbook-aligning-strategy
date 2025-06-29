import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
from datetime import datetime, timedelta

# Page configuration
st.set_page_config(
    page_title="AI Strategy Mapper", 
    layout="wide",
    initial_sidebar_state="expanded",
    page_icon="📊"
)

# Custom CSS for professional styling
st.markdown("""
<style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    /* Global styling */
    .main {
        font-family: 'Inter', sans-serif;
    }
    
    /* Custom header styling */
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 10px;
        margin-bottom: 2rem;
        color: white;
    }
    
    .main-header h1 {
        color: white !important;
        font-weight: 700;
        font-size: 2.5rem;
        margin-bottom: 0.5rem;
    }
    
    .main-header p {
        color: rgba(255, 255, 255, 0.9);
        font-size: 1.1rem;
        margin-bottom: 0;
    }
    
    /* Card styling */
    .info-card {
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
        border-left: 4px solid #667eea;
        margin-bottom: 1.5rem;
    }
    
    .metric-card {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        padding: 1.5rem;
        border-radius: 10px;
        text-align: center;
        margin-bottom: 1rem;
    }
    
    /* Step indicator styling */
    .step-indicator {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 20px;
        font-weight: 500;
        display: inline-block;
        margin-bottom: 1rem;
    }
    
    /* Button styling */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.5rem 1.5rem;
        font-weight: 500;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
    }
    
    /* Navigation button styling */
    .nav-button-container {
        background: #f8f9fa;
        padding: 1.5rem;
        border-radius: 10px;
        margin-top: 2rem;
    }
    
    /* Progress bar styling */
    .stProgress .st-bo {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
    }
    
    /* Sidebar styling */
    .css-1d391kg {
        background: linear-gradient(180deg, #f8f9fa 0%, #e9ecef 100%);
    }
    
    /* Form styling */
    .stForm {
        background: white;
        padding: 2rem;
        border-radius: 10px;
        box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
        border: 1px solid #e9ecef;
    }
    
    /* Expander styling */
    .streamlit-expanderHeader {
        background: #f8f9fa;
        border-radius: 8px;
        font-weight: 500;
    }
    
    /* Success/Warning/Error styling */
    .stSuccess {
        background: linear-gradient(135deg, #d4edda 0%, #c3e6cb 100%);
        border-left: 4px solid #28a745;
    }
    
    .stWarning {
        background: linear-gradient(135deg, #fff3cd 0%, #ffeaa7 100%);
        border-left: 4px solid #ffc107;
    }
    
    .stError {
        background: linear-gradient(135deg, #f8d7da 0%, #f5c6cb 100%);
        border-left: 4px solid #dc3545;
    }
    
    /* Table styling */
    .dataframe {
        border: none !important;
        border-radius: 10px;
        overflow: hidden;
    }
    
    .dataframe thead tr th {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
    }
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Custom metric styling */
    .custom-metric {
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
        text-align: center;
        margin-bottom: 1rem;
    }
    
    .custom-metric h3 {
        color: #667eea;
        font-size: 2rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
    }
    
    .custom-metric p {
        color: #6c757d;
        font-size: 0.9rem;
        margin: 0;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'initiatives' not in st.session_state:
    st.session_state.initiatives = []
if 'stakeholders' not in st.session_state:
    st.session_state.stakeholders = []
if 'goals' not in st.session_state:
    st.session_state.goals = []
if 'current_page' not in st.session_state:
    st.session_state.current_page = "Strategic Overview"

# Professional Header
st.markdown("""
<div class="main-header">
    <h1>AI Strategy Mapper</h1>
    <p>Chapter 3 Tool: Transform business objectives into actionable AI initiatives using proven strategic frameworks</p>
    <p style="font-size: 0.9rem; margin-top: 1rem; opacity: 0.9;">
        Part of the <strong>AI Playbook for Organisations</strong> toolkit by Madhusudhan Konda
    </p>
</div>
""", unsafe_allow_html=True)

# Define page flow
PAGE_ORDER = [
    "Strategic Overview",
    "1. Goal Decomposition", 
    "2. Capability Assessment",
    "3. Initiative Definition",
    "4. Impact Estimation",
    "Portfolio Matrix",
    "Stakeholder Alignment",
    "ROI Calculator",
    "Action Plan"
]

# Professional Sidebar
with st.sidebar:
    st.markdown("### Progress Dashboard")
    
    current_index = PAGE_ORDER.index(st.session_state.current_page)
    progress = (current_index + 1) / len(PAGE_ORDER)
    
    # Progress indicator with custom styling
    st.markdown(f"""
    <div class="step-indicator">
        Step {current_index + 1} of {len(PAGE_ORDER)} • {progress:.0%} Complete
    </div>
    """, unsafe_allow_html=True)
    
    st.progress(progress)
    
    # Portfolio metrics (if data exists)
    if st.session_state.initiatives:
        st.markdown("### Portfolio Metrics")
        
        total_initiatives = len(st.session_state.initiatives)
        high_impact = sum(1 for i in st.session_state.initiatives if i.get('business_impact', 'Medium') == 'High')
        total_investment = sum(float(i.get('investment_required', 0)) for i in st.session_state.initiatives)
        
        col1, col2 = st.columns(2)
        with col1:
            st.markdown(f"""
            <div class="custom-metric">
                <h3>{total_initiatives}</h3>
                <p>Total Initiatives</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div class="custom-metric">
                <h3>{high_impact}</h3>
                <p>High Impact</p>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown(f"""
        <div class="custom-metric">
            <h3>${total_investment:,.0f}</h3>
            <p>Total Investment</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    st.markdown("### Quick Navigation")
    st.markdown("*Jump to any step:*")
    
    # Navigation buttons in sidebar
    for i, page_name in enumerate(PAGE_ORDER):
        is_current = page_name == st.session_state.current_page
        is_completed = i < current_index
        
        # Style based on status
        if is_current:
            button_style = "►"
        elif is_completed:
            button_style = "✓"
        else:
            button_style = "○"
        
        if st.button(f"{button_style} {page_name}", key=f"nav_{i}", use_container_width=True):
            st.session_state.current_page = page_name
            st.rerun()
    
    # AI Playbook Toolkit section
    st.markdown("---")
    st.markdown("### 📚 AI Playbook Toolkit")
    st.markdown("""
    **Other Tools in the Series:**
    
    🔍 [**Ch2: AI Readiness Assessment**](https://aiready.streamlit.app/)  
    *Evaluate your organization's AI readiness*
    
    🎯 **Ch3: AI Strategy Mapper** *(current)*  
    *Align AI initiatives with business goals*
    
    📖 [**Read the Book**](https://medium.com/ai-playbook-for-organisations)  
    *AI Playbook for Organisations*
    """)

page = st.session_state.current_page

# Navigation buttons
def show_navigation_buttons():
    col1, col2, col3 = st.columns([1, 2, 1])
    
    current_index = PAGE_ORDER.index(st.session_state.current_page)
    
    with col1:
        if current_index > 0:
            if st.button("← Previous Step", key="prev_btn", use_container_width=True):
                st.session_state.current_page = PAGE_ORDER[current_index - 1]
                st.rerun()
    
    with col3:
        if current_index < len(PAGE_ORDER) - 1:
            if st.button("Next Step →", key="next_btn", use_container_width=True):
                st.session_state.current_page = PAGE_ORDER[current_index + 1]
                st.rerun()

# Function to display navigation buttons with current position
st.markdown("---")
col1, col2, col3 = st.columns([1, 2, 1])

current_index = PAGE_ORDER.index(st.session_state.current_page)

with col1:
    if current_index > 0:
        if st.button("← Previous Step", key="main_prev", use_container_width=True):
            st.session_state.current_page = PAGE_ORDER[current_index - 1]
            st.rerun()

with col2:
    st.markdown(f"<div style='text-align: center; padding: 10px;'><strong>Step {current_index + 1} of {len(PAGE_ORDER)}</strong></div>", unsafe_allow_html=True)

with col3:
    if current_index < len(PAGE_ORDER) - 1:
        if st.button("Next Step →", key="main_next", use_container_width=True):
            st.session_state.current_page = PAGE_ORDER[current_index + 1]
            st.rerun()

# Strategic Overview Page
if page == "Strategic Overview":
    st.markdown("## Strategic AI Mapping Process")
    
    # Process overview cards
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### The 4-Step Process")
        st.markdown("""
        **1. Goal Decomposition**  
        Break broad business objectives into specific, measurable AI-relevant goals
        
        **2. Capability Assessment**  
        Evaluate your organization's readiness (data, skills, infrastructure)
        
        **3. Initiative Definition**  
        Define concrete AI projects with clear ownership and phases
        
        **4. Impact Estimation**  
        Calculate expected business value and resource requirements
        """)
    
    with col2:
        st.markdown("### Key Principles")
        st.markdown("""
        **Business-First**  
        Start with problems, not technology
        
        **Value-Driven**  
        Every initiative must have measurable business impact
        
        **Stakeholder-Centric**  
        Involve all affected parties early
        
        **Risk-Aware**  
        Balance innovation with operational stability
        """)
    
    # Portfolio overview (if initiatives exist)
    if st.session_state.initiatives:
        st.markdown("## Current Portfolio Overview")
        
        col1, col2, col3, col4 = st.columns(4)
        
        total_initiatives = len(st.session_state.initiatives)
        high_impact = sum(1 for i in st.session_state.initiatives if i.get('business_impact', 'Medium') == 'High')
        total_investment = sum(float(i.get('investment_required', 0)) for i in st.session_state.initiatives)
        avg_roi = np.mean([float(i.get('expected_roi', 0)) for i in st.session_state.initiatives])
        
        with col1:
            st.metric("Total Initiatives", total_initiatives)
        
        with col2:
            st.metric("High Impact", high_impact)
        
        with col3:
            st.metric("Total Investment", f"${total_investment:,.0f}")
        
        with col4:
            st.metric("Avg. Expected ROI", f"{avg_roi:.1f}%")
    else:
        st.markdown("### Ready to Get Started?")
        st.info("""
        Begin your AI strategy journey by defining your business objectives and goals. 
        This tool will guide you through a proven 4-step process used by leading organizations 
        to align AI initiatives with business value.
        
        **Time investment:** 30-45 minutes for a comprehensive strategy mapping
        """)
    
    show_navigation_buttons()

# Goal Decomposition Page
elif page == "1. Goal Decomposition":
    st.markdown("## Step 1: Goal Decomposition")
    
    st.info("Break down broad business objectives into specific, measurable, AI-relevant goals that drive meaningful outcomes.")
    
    # Business objective input
    st.markdown("### Primary Business Objective")
    business_objective = st.text_area(
        "What is your main business challenge or opportunity?",
        placeholder="Example: Reduce customer churn by 15% while improving customer satisfaction",
        help="Be specific about what you want to achieve"
    )
    
    # Goals definition
    st.markdown("### Decomposed Goals")
    st.markdown("Break down your objective into specific, measurable AI-relevant goals.")
    
    # Add new goal
    with st.container():
        col1, col2 = st.columns([3, 1])
        
        with col1:
            new_goal = st.text_input(
                "Goal Description",
                placeholder="Example: Implement predictive analytics to identify at-risk customers",
                label_visibility="collapsed"
            )
        
        with col2:
            if st.button("Add Goal", use_container_width=True):
                if new_goal and new_goal not in st.session_state.goals:
                    st.session_state.goals.append(new_goal)
                    st.rerun()
    
    # Display existing goals
    if st.session_state.goals:
        st.markdown("### Goal Summary")
        for i, goal in enumerate(st.session_state.goals):
            col1, col2 = st.columns([4, 1])
            with col1:
                st.write(f"{i+1}. {goal}")
            with col2:
                if st.button("Remove", key=f"remove_goal_{i}"):
                    st.session_state.goals.pop(i)
                    st.rerun()
    
    # Save button
    if st.button("Save Goals", use_container_width=True):
        st.session_state.business_objective = business_objective
        st.success("✓ Goals saved successfully!")
        
        # Auto-advance
        if st.session_state.goals:
            st.session_state.current_page = "2. Capability Assessment"
            st.rerun()
    
    show_navigation_buttons()

# Capability Assessment Page
elif page == "2. Capability Assessment":
    st.header("Step 2: Capability Assessment")
    st.markdown("Evaluate your organization's readiness across key dimensions.")
    
    st.subheader("Assessment Dimensions")
    
    # Data Readiness
    with st.expander("Data Readiness", expanded=True):
        data_quality = st.selectbox("Data Quality", ["Poor", "Fair", "Good", "Excellent"])
        data_availability = st.selectbox("Data Availability", ["Limited", "Partial", "Good", "Comprehensive"])
        data_governance = st.selectbox("Data Governance", ["None", "Basic", "Structured", "Advanced"])
    
    # Technical Capabilities
    with st.expander("Technical Capabilities"):
        ai_expertise = st.selectbox("AI/ML Expertise", ["None", "Basic", "Intermediate", "Advanced"])
        infrastructure = st.selectbox("Technical Infrastructure", ["Legacy", "Hybrid", "Modern", "Cloud-native"])
        dev_ops = st.selectbox("MLOps Maturity", ["None", "Basic", "Intermediate", "Advanced"])
    
    # Organizational Readiness
    with st.expander("Organizational Readiness"):
        leadership_support = st.selectbox("Leadership Support", ["Low", "Medium", "High", "Very High"])
        change_readiness = st.selectbox("Change Management", ["Poor", "Fair", "Good", "Excellent"])
        budget_availability = st.selectbox("Budget Availability", ["Limited", "Moderate", "Good", "Generous"])
    
    # Calculate overall readiness score
    scores = {
        "Poor": 1, "None": 1, "Legacy": 1, "Low": 1, "Limited": 1,
        "Fair": 2, "Basic": 2, "Medium": 2, "Partial": 2, "Moderate": 2,
        "Good": 3, "Intermediate": 3, "High": 3, "Structured": 3,
        "Excellent": 4, "Advanced": 4, "Very High": 4, "Comprehensive": 4,
        "Modern": 4, "Cloud-native": 4, "Generous": 4
    }
    
    total_score = (scores.get(data_quality, 0) + scores.get(data_availability, 0) + 
                   scores.get(data_governance, 0) + scores.get(ai_expertise, 0) + 
                   scores.get(infrastructure, 0) + scores.get(dev_ops, 0) + 
                   scores.get(leadership_support, 0) + scores.get(change_readiness, 0) + 
                   scores.get(budget_availability, 0))
    
    readiness_percentage = (total_score / 36) * 100
    
    # Display readiness score
    st.subheader("Overall Readiness Score")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Readiness Score", f"{readiness_percentage:.0f}%")
        if readiness_percentage >= 75:
            st.success("High readiness - Ready for complex AI initiatives")
        elif readiness_percentage >= 50:
            st.warning("Medium readiness - Start with focused pilots")
        else:
            st.error("Low readiness - Foundation building needed")
    
    with col2:
        # Readiness radar chart
        categories = ['Data Quality', 'Data Availability', 'Data Governance', 
                     'AI Expertise', 'Infrastructure', 'MLOps', 
                     'Leadership', 'Change Mgmt', 'Budget']
        values = [scores.get(data_quality, 0), scores.get(data_availability, 0),
                 scores.get(data_governance, 0), scores.get(ai_expertise, 0),
                 scores.get(infrastructure, 0), scores.get(dev_ops, 0),
                 scores.get(leadership_support, 0), scores.get(change_readiness, 0),
                 scores.get(budget_availability, 0)]
        
        fig = go.Figure()
        fig.add_trace(go.Scatterpolar(
            r=values,
            theta=categories,
            fill='toself',
            name='Current State'
        ))
        fig.update_layout(
            polar=dict(radialaxis=dict(visible=True, range=[0, 4])),
            showlegend=True,
            height=400
        )
        st.plotly_chart(fig, use_container_width=True)
    
    if st.button("Save Capability Assessment"):
        st.session_state.capability_assessment = {
            "readiness_score": readiness_percentage,
            "scores": {
                "data_quality": data_quality,
                "data_availability": data_availability,
                "data_governance": data_governance,
                "ai_expertise": ai_expertise,
                "infrastructure": infrastructure,
                "dev_ops": dev_ops,
                "leadership_support": leadership_support,
                "change_readiness": change_readiness,
                "budget_availability": budget_availability
            }
        }
        st.success("Assessment saved! Proceed to Initiative Definition.")
    
    st.markdown("---")
    show_navigation_buttons()

# Initiative Definition Page
elif page == "3. Initiative Definition":
    st.header("Step 3: Initiative Definition")
    st.markdown("Define concrete AI initiatives with clear scope, ownership, and phases.")
    
    with st.form("initiative_form"):
        st.subheader("New AI Initiative")
        
        col1, col2 = st.columns(2)
        
        with col1:
            name = st.text_input("Initiative Name", placeholder="e.g., Customer Churn Prediction")
            business_problem = st.text_area("Business Problem", 
                placeholder="Describe the specific business problem this will solve")
            ai_solution = st.text_area("AI Solution", 
                placeholder="Describe the AI approach and technology")
        
        with col2:
            owner = st.text_input("Initiative Owner", placeholder="Name and department")
            timeline = st.selectbox("Timeline", ["3-6 months", "6-12 months", "12+ months"])
            complexity = st.selectbox("Technical Complexity", ["Low", "Medium", "High"])
            business_impact = st.selectbox("Expected Business Impact", ["Low", "Medium", "High"])
        
        # Phases
        st.subheader("Implementation Phases")
        phase1 = st.text_input("Phase 1 (Pilot)", placeholder="e.g., Train model and test on historical data")
        phase2 = st.text_input("Phase 2 (MVP)", placeholder="e.g., Run controlled pilot with business users")
        phase3 = st.text_input("Phase 3 (Scale)", placeholder="e.g., Roll out to all business units")
        
        # Success metrics
        st.subheader("Success Metrics")
        primary_metric = st.text_input("Primary Metric", placeholder="e.g., Reduce churn rate by 20%")
        secondary_metrics = st.text_area("Secondary Metrics", 
            placeholder="e.g., Improve customer lifetime value, Reduce support tickets")
        
        submitted = st.form_submit_button("Add Initiative")
        
        if submitted and name and business_problem:
            initiative = {
                "name": name,
                "business_problem": business_problem,
                "ai_solution": ai_solution,
                "owner": owner,
                "timeline": timeline,
                "complexity": complexity,
                "business_impact": business_impact,
                "phase1": phase1,
                "phase2": phase2,
                "phase3": phase3,
                "primary_metric": primary_metric,
                "secondary_metrics": secondary_metrics,
                "created_at": datetime.now().strftime("%Y-%m-%d %H:%M")
            }
            st.session_state.initiatives.append(initiative)
            st.success(f"Initiative '{name}' added successfully!")
            st.rerun()
    
    # Display existing initiatives
    if st.session_state.initiatives:
        st.subheader("Current Initiatives")
        for i, initiative in enumerate(st.session_state.initiatives):
            with st.expander(f"{initiative['name']} - {initiative['business_impact']} Impact"):
                col1, col2 = st.columns(2)
                with col1:
                    st.write(f"**Problem:** {initiative['business_problem']}")
                    st.write(f"**Solution:** {initiative['ai_solution']}")
                    st.write(f"**Owner:** {initiative['owner']}")
                with col2:
                    st.write(f"**Timeline:** {initiative['timeline']}")
                    st.write(f"**Complexity:** {initiative['complexity']}")
                    st.write(f"**Primary Metric:** {initiative['primary_metric']}")
                
                if st.button(f"Remove", key=f"remove_{i}"):
                    st.session_state.initiatives.pop(i)
                    st.rerun()

# Impact Estimation Page
elif page == "4. Impact Estimation":
    st.header("Step 4: Impact Estimation")
    st.markdown("Calculate expected business value and resource requirements for each initiative.")
    
    if not st.session_state.initiatives:
        st.warning("Please define some initiatives first in Step 3.")
    else:
        # Select initiative to analyze
        initiative_names = [i['name'] for i in st.session_state.initiatives]
        selected_initiative = st.selectbox("Select Initiative to Analyze", initiative_names)
        
        if selected_initiative:
            # Find the selected initiative
            initiative = next(i for i in st.session_state.initiatives if i['name'] == selected_initiative)
            
            st.subheader(f"Impact Analysis: {selected_initiative}")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader("Financial Impact")
                cost_savings = st.number_input("Annual Cost Savings ($)", min_value=0.0, step=1000.0)
                revenue_increase = st.number_input("Annual Revenue Increase ($)", min_value=0.0, step=1000.0)
                risk_reduction = st.number_input("Risk Reduction Value ($)", min_value=0.0, step=1000.0)
                
                st.subheader("💸 Investment Required")
                technology_cost = st.number_input("Technology Costs ($)", min_value=0.0, step=1000.0)
                personnel_cost = st.number_input("Personnel Costs ($)", min_value=0.0, step=1000.0)
                infrastructure_cost = st.number_input("Infrastructure Costs ($)", min_value=0.0, step=1000.0)
            
            with col2:
                st.subheader("Operational Impact")
                efficiency_gain = st.slider("Process Efficiency Gain (%)", 0, 100, 10)
                quality_improvement = st.slider("Quality Improvement (%)", 0, 100, 5)
                time_savings = st.slider("Time Savings (%)", 0, 100, 15)
                
                st.subheader("Risk Assessment")
                technical_risk = st.selectbox("Technical Risk", ["Low", "Medium", "High"])
                business_risk = st.selectbox("Business Risk", ["Low", "Medium", "High"])
                timeline_risk = st.selectbox("Timeline Risk", ["Low", "Medium", "High"])
            
            # Calculate ROI and payback
            total_benefits = cost_savings + revenue_increase + risk_reduction
            total_investment = technology_cost + personnel_cost + infrastructure_cost
            
            if total_investment > 0:
                roi = ((total_benefits - total_investment) / total_investment) * 100
                payback_period = total_investment / total_benefits if total_benefits > 0 else float('inf')
            else:
                roi = 0
                payback_period = float('inf')
            
            # Display results
            st.subheader("Financial Analysis")
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("Total Benefits", f"${total_benefits:,.0f}")
            with col2:
                st.metric("Total Investment", f"${total_investment:,.0f}")
            with col3:
                st.metric("Expected ROI", f"{roi:.1f}%")
            with col4:
                if payback_period != float('inf'):
                    st.metric("Payback Period", f"{payback_period:.1f} years")
                else:
                    st.metric("Payback Period", "N/A")
            
            # Save impact data
            if st.button("Save Impact Analysis"):
                # Update the initiative with impact data
                for i, init in enumerate(st.session_state.initiatives):
                    if init['name'] == selected_initiative:
                        st.session_state.initiatives[i].update({
                            'cost_savings': cost_savings,
                            'revenue_increase': revenue_increase,
                            'risk_reduction': risk_reduction,
                            'technology_cost': technology_cost,
                            'personnel_cost': personnel_cost,
                            'infrastructure_cost': infrastructure_cost,
                            'total_benefits': total_benefits,
                            'investment_required': total_investment,
                            'expected_roi': roi,
                            'payback_period': payback_period,
                            'efficiency_gain': efficiency_gain,
                            'quality_improvement': quality_improvement,
                            'time_savings': time_savings,
                            'technical_risk': technical_risk,
                            'business_risk': business_risk,
                            'timeline_risk': timeline_risk
                        })
                        break
                st.success("Impact analysis saved!")

# Portfolio Matrix Page
elif page == "Portfolio Matrix":
    st.header("AI Initiative Portfolio Matrix")
    st.markdown("Visualize your AI initiatives by complexity vs. business impact to guide prioritization.")
    
    if not st.session_state.initiatives:
        st.warning("Please define some initiatives first.")
    else:
        # Create portfolio matrix
        initiatives_with_scores = []
        for init in st.session_state.initiatives:
            complexity_score = {"Low": 1, "Medium": 2, "High": 3}.get(init.get('complexity', 'Medium'), 2)
            impact_score = {"Low": 1, "Medium": 2, "High": 3}.get(init.get('business_impact', 'Medium'), 2)
            
            initiatives_with_scores.append({
                'name': init['name'],
                'complexity': complexity_score,
                'impact': impact_score,
                'investment': init.get('investment_required', 0),
                'roi': init.get('expected_roi', 0)
            })
        
        df = pd.DataFrame(initiatives_with_scores)
        
        # Create scatter plot
        fig = px.scatter(
            df, 
            x='complexity', 
            y='impact',
            size='investment',
            color='roi',
            hover_name='name',
            title="AI Initiative Portfolio Matrix",
            labels={
                'complexity': 'Technical Complexity',
                'impact': 'Business Impact',
                'roi': 'Expected ROI (%)'
            },
            color_continuous_scale='RdYlGn'
        )
        
        # Update axes
        fig.update_xaxes(
            tickvals=[1, 2, 3],
            ticktext=['Low', 'Medium', 'High'],
            range=[0.5, 3.5]
        )
        fig.update_yaxes(
            tickvals=[1, 2, 3],
            ticktext=['Low', 'Medium', 'High'],
            range=[0.5, 3.5]
        )
        
        # Add quadrant lines
        fig.add_hline(y=2.5, line_dash="dash", line_color="gray", opacity=0.5)
        fig.add_vline(x=2.5, line_dash="dash", line_color="gray", opacity=0.5)
        
        # Add quadrant labels
        fig.add_annotation(x=1.25, y=3.25, text="Quick Wins<br>(Low Complexity, High Impact)", 
                          showarrow=False, font_color="green")
        fig.add_annotation(x=3.25, y=3.25, text="Strategic Bets<br>(High Complexity, High Impact)", 
                          showarrow=False, font_color="blue")
        fig.add_annotation(x=1.25, y=0.75, text="Fill-ins<br>(Low Complexity, Low Impact)", 
                          showarrow=False, font_color="orange")
        fig.add_annotation(x=3.25, y=0.75, text="Question Marks<br>(High Complexity, Low Impact)", 
                          showarrow=False, font_color="red")
        
        fig.update_layout(height=600, width=800)
        st.plotly_chart(fig, use_container_width=True)
        
        # Recommendations
        st.subheader("Portfolio Recommendations")
        
        quick_wins = df[(df['complexity'] <= 2) & (df['impact'] >= 2.5)]
        strategic_bets = df[(df['complexity'] >= 2.5) & (df['impact'] >= 2.5)]
        question_marks = df[(df['complexity'] >= 2.5) & (df['impact'] <= 2)]
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.subheader("Priority 1: Quick Wins")
            if not quick_wins.empty:
                for _, init in quick_wins.iterrows():
                    st.write(f"• {init['name']}")
            else:
                st.write("No quick wins identified")
        
        with col2:
            st.subheader("Priority 2: Strategic Bets")
            if not strategic_bets.empty:
                for _, init in strategic_bets.iterrows():
                    st.write(f"• {init['name']}")
            else:
                st.write("No strategic bets identified")
        
        with col3:
            st.subheader("❓ Review Needed")
            if not question_marks.empty:
                st.write("High complexity, low impact initiatives:")
                for _, init in question_marks.iterrows():
                    st.write(f"• {init['name']}")
            else:
                st.write("No initiatives need review")

# Stakeholder Alignment Page
elif page == "Stakeholder Alignment":
    st.header("Stakeholder Alignment Management")
    st.markdown("Map and manage stakeholder engagement for your AI initiatives.")
    
    # Add new stakeholder
    with st.form("stakeholder_form"):
        st.subheader("Add Stakeholder")
        
        col1, col2 = st.columns(2)
        with col1:
            stakeholder_name = st.text_input("Name")
            role = st.text_input("Role/Department")
            influence = st.selectbox("Influence Level", ["Low", "Medium", "High", "Very High"])
        
        with col2:
            interest = st.selectbox("Interest Level", ["Low", "Medium", "High", "Very High"])
            sentiment = st.selectbox("Current Sentiment", ["Skeptical", "Neutral", "Supportive", "Champion"])
            concerns = st.text_area("Key Concerns")
        
        if st.form_submit_button("Add Stakeholder"):
            if stakeholder_name and role:
                stakeholder = {
                    "name": stakeholder_name,
                    "role": role,
                    "influence": influence,
                    "interest": interest,
                    "sentiment": sentiment,
                    "concerns": concerns,
                    "added_at": datetime.now().strftime("%Y-%m-%d")
                }
                st.session_state.stakeholders.append(stakeholder)
                st.success(f"Stakeholder '{stakeholder_name}' added!")
                st.rerun()
    
    # Display stakeholder matrix
    if st.session_state.stakeholders:
        st.subheader("Stakeholder Influence-Interest Matrix")
        
        # Prepare data for plotting
        stakeholder_data = []
        for stakeholder in st.session_state.stakeholders:
            influence_score = {"Low": 1, "Medium": 2, "High": 3, "Very High": 4}.get(stakeholder['influence'], 2)
            interest_score = {"Low": 1, "Medium": 2, "High": 3, "Very High": 4}.get(stakeholder['interest'], 2)
            sentiment_color = {"Skeptical": "red", "Neutral": "yellow", "Supportive": "lightgreen", "Champion": "green"}.get(stakeholder['sentiment'], "gray")
            
            stakeholder_data.append({
                'name': stakeholder['name'],
                'role': stakeholder['role'],
                'influence': influence_score,
                'interest': interest_score,
                'sentiment': stakeholder['sentiment'],
                'concerns': stakeholder['concerns']
            })
        
        df_stakeholders = pd.DataFrame(stakeholder_data)
        
        fig = px.scatter(
            df_stakeholders,
            x='interest',
            y='influence',
            color='sentiment',
            hover_name='name',
            hover_data=['role', 'concerns'],
            title="Stakeholder Influence-Interest Matrix",
            labels={'interest': 'Interest Level', 'influence': 'Influence Level'},
            color_discrete_map={
                'Skeptical': 'red',
                'Neutral': 'yellow', 
                'Supportive': 'lightgreen',
                'Champion': 'green'
            }
        )
        
        fig.update_xaxes(tickvals=[1,2,3,4], ticktext=['Low','Medium','High','Very High'])
        fig.update_yaxes(tickvals=[1,2,3,4], ticktext=['Low','Medium','High','Very High'])
        
        # Add quadrant lines
        fig.add_hline(y=2.5, line_dash="dash", line_color="gray", opacity=0.5)
        fig.add_vline(x=2.5, line_dash="dash", line_color="gray", opacity=0.5)
        
        fig.update_layout(height=500)
        st.plotly_chart(fig, use_container_width=True)
        
        # Engagement strategies
        st.subheader("Engagement Strategies")
        col1, col2 = st.columns(2)
        
        with col1:
            high_influence_high_interest = df_stakeholders[(df_stakeholders['influence'] >= 3) & (df_stakeholders['interest'] >= 3)]
            st.subheader("Manage Closely")
            st.write("High influence, high interest - Key decision makers")
            for _, s in high_influence_high_interest.iterrows():
                st.write(f"• **{s['name']}** ({s['role']}) - {s['sentiment']}")
        
        with col2:
            high_influence_low_interest = df_stakeholders[(df_stakeholders['influence'] >= 3) & (df_stakeholders['interest'] < 3)]
            st.subheader("📢 Keep Satisfied")
            st.write("High influence, low interest - Need regular updates")
            for _, s in high_influence_low_interest.iterrows():
                st.write(f"• **{s['name']}** ({s['role']}) - {s['sentiment']}")
    
    st.markdown("---")
    show_navigation_buttons()

# ROI Calculator Page
elif page == "ROI Calculator":
    st.header("AI Initiative ROI Calculator")
    st.markdown("Calculate detailed return on investment for AI initiatives using multiple scenarios.")
    
    # Scenario-based calculator
    st.subheader("Scenario Analysis")
    
    # Base inputs
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Investment Costs")
        initial_investment = st.number_input("Initial Investment ($)", min_value=0.0, step=10000.0, value=100000.0)
        annual_operating = st.number_input("Annual Operating Costs ($)", min_value=0.0, step=5000.0, value=25000.0)
        implementation_time = st.number_input("Implementation Time (months)", min_value=1, max_value=36, value=6)
    
    with col2:
        st.subheader("Benefit Categories")
        cost_reduction = st.number_input("Annual Cost Reduction ($)", min_value=0.0, step=10000.0, value=150000.0)
        revenue_increase = st.number_input("Annual Revenue Increase ($)", min_value=0.0, step=10000.0, value=75000.0)
        productivity_gain = st.number_input("Annual Productivity Value ($)", min_value=0.0, step=5000.0, value=50000.0)
    
    # Scenario modeling
    st.subheader("Scenario Modeling")
    conservative_factor = st.slider("Conservative Scenario (%)", 50, 90, 70) / 100
    optimistic_factor = st.slider("Optimistic Scenario (%)", 110, 200, 130) / 100
    
    # Calculate scenarios
    annual_benefits = cost_reduction + revenue_increase + productivity_gain
    
    scenarios = {
        "Conservative": annual_benefits * conservative_factor,
        "Base Case": annual_benefits,
        "Optimistic": annual_benefits * optimistic_factor
    }
    
    # Multi-year analysis
    years = st.selectbox("Analysis Period (years)", [1, 2, 3, 5], index=2)
    
    # Calculate NPV and ROI for each scenario
    discount_rate = 0.1  # 10% discount rate
    
    results = []
    for scenario_name, annual_benefit in scenarios.items():
        npv = -initial_investment
        for year in range(1, years + 1):
            if year <= implementation_time / 12:
                # Reduced benefits during implementation
                benefit = annual_benefit * (year / (implementation_time / 12)) * 0.5
            else:
                benefit = annual_benefit
            
            net_cash_flow = benefit - annual_operating
            discounted_cash_flow = net_cash_flow / ((1 + discount_rate) ** year)
            npv += discounted_cash_flow
        
        roi = (npv / initial_investment) * 100
        payback = initial_investment / (annual_benefit - annual_operating) if annual_benefit > annual_operating else float('inf')
        
        results.append({
            "Scenario": scenario_name,
            "Annual Benefits": f"${annual_benefit:,.0f}",
            "NPV": f"${npv:,.0f}",
            "ROI": f"{roi:.1f}%",
            "Payback (years)": f"{payback:.1f}" if payback != float('inf') else "N/A"
        })
    
    # Display results
    st.subheader("Financial Analysis Results")
    results_df = pd.DataFrame(results)
    st.dataframe(results_df, use_container_width=True)
    
    # Visualization
    col1, col2 = st.columns(2)
    
    with col1:
        # NPV comparison
        npv_values = [float(r["NPV"].replace("$", "").replace(",", "")) for r in results]
        fig_npv = px.bar(
            x=["Conservative", "Base Case", "Optimistic"],
            y=npv_values,
            title="Net Present Value by Scenario",
            labels={"x": "Scenario", "y": "NPV ($)"}
        )
        st.plotly_chart(fig_npv, use_container_width=True)
    
    with col2:
        # ROI comparison
        roi_values = [float(r["ROI"].replace("%", "")) for r in results]
        fig_roi = px.bar(
            x=["Conservative", "Base Case", "Optimistic"],
            y=roi_values,
            title="Return on Investment by Scenario",
            labels={"x": "Scenario", "y": "ROI (%)"}
        )
        st.plotly_chart(fig_roi, use_container_width=True)
    
    # Risk assessment
    st.subheader("Risk Factors")
    risk_factors = st.multiselect(
        "Select applicable risk factors:",
        [
            "Data quality issues",
            "Technical complexity",
            "User adoption resistance", 
            "Regulatory changes",
            "Competition",
            "Technology obsolescence",
            "Integration challenges",
            "Skill shortage"
        ]
    )
    
    if risk_factors:
        risk_impact = len(risk_factors) * 5  # 5% impact per risk factor
        st.warning(f"Identified {len(risk_factors)} risk factors. Consider reducing expected benefits by {risk_impact}% to account for risks.")
    
    st.markdown("---")
    show_navigation_buttons()

# Action Plan Page
elif page == "Action Plan":
    st.header("AI Strategy Action Plan")
    st.markdown("Generate a comprehensive action plan based on your strategic mapping.")
    
    if not st.session_state.initiatives:
        st.warning("Please complete the strategic mapping process first.")
    else:
        # Summary of current state
        st.subheader("Executive Summary")
        
        total_initiatives = len(st.session_state.initiatives)
        high_impact_initiatives = sum(1 for i in st.session_state.initiatives if i.get('business_impact') == 'High')
        total_investment = sum(i.get('investment_required', 0) for i in st.session_state.initiatives)
        avg_roi = np.mean([i.get('expected_roi', 0) for i in st.session_state.initiatives])
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total Initiatives", total_initiatives)
        with col2:
            st.metric("High Impact Initiatives", high_impact_initiatives)
        with col3:
            st.metric("Total Investment", f"${total_investment:,.0f}")
        with col4:
            st.metric("Average Expected ROI", f"{avg_roi:.1f}%")
        
        # Prioritized roadmap
        st.subheader("Prioritized Implementation Roadmap")
        
        # Sort initiatives by priority (quick wins first, then strategic bets)
        def get_priority_score(initiative):
            complexity_score = {"Low": 1, "Medium": 2, "High": 3}.get(initiative.get('complexity', 'Medium'), 2)
            impact_score = {"Low": 1, "Medium": 2, "High": 3}.get(initiative.get('business_impact', 'Medium'), 2)
            roi = initiative.get('expected_roi', 0)
            
            # Quick wins (low complexity, high impact) get highest priority
            if complexity_score <= 2 and impact_score >= 2:
                return 100 + roi
            # Strategic bets (high complexity, high impact) get second priority
            elif complexity_score >= 2 and impact_score >= 2:
                return 50 + roi
            # Others get lower priority
            else:
                return roi
        
        sorted_initiatives = sorted(st.session_state.initiatives, key=get_priority_score, reverse=True)
        
        # Timeline visualization
        timeline_data = []
        current_date = datetime.now()
        
        for i, initiative in enumerate(sorted_initiatives[:5]):  # Top 5 initiatives
            timeline_map = {"3-6 months": 4, "6-12 months": 9, "12+ months": 18}
            duration = timeline_map.get(initiative.get('timeline', '6-12 months'), 9)
            
            start_date = current_date + timedelta(days=i*30)  # Stagger starts
            end_date = start_date + timedelta(days=duration*30)
            
            timeline_data.append({
                "Initiative": initiative['name'],
                "Start": start_date,
                "End": end_date,
                "Impact": initiative.get('business_impact', 'Medium'),
                "Investment": initiative.get('investment_required', 0)
            })
        
        if timeline_data:
            timeline_df = pd.DataFrame(timeline_data)
            
            fig = px.timeline(
                timeline_df,
                x_start="Start",
                x_end="End", 
                y="Initiative",
                color="Impact",
                title="Implementation Timeline (Top 5 Priorities)",
                color_discrete_map={"Low": "lightblue", "Medium": "orange", "High": "red"}
            )
            fig.update_layout(height=400)
            st.plotly_chart(fig, use_container_width=True)
        
        # Next steps by quarter
        st.subheader("Quarterly Action Items")
        
        quarters = ["Q1 2024", "Q2 2024", "Q3 2024", "Q4 2024"]
        
        for i, quarter in enumerate(quarters):
            with st.expander(f"{quarter} - Focus Areas"):
                if i < len(sorted_initiatives):
                    initiative = sorted_initiatives[i]
                    st.write(f"**Primary Initiative:** {initiative['name']}")
                    st.write(f"**Business Problem:** {initiative.get('business_problem', 'N/A')}")
                    st.write(f"**Owner:** {initiative.get('owner', 'TBD')}")
                    
                    # Phase breakdown
                    if initiative.get('phase1'):
                        st.write(f"**Phase 1:** {initiative['phase1']}")
                    if initiative.get('phase2'):
                        st.write(f"**Phase 2:** {initiative['phase2']}")
                    
                    # Key actions
                    st.write("**Key Actions:**")
                    if i == 0:
                        st.write("• Finalize data requirements and access")
                        st.write("• Assemble project team")
                        st.write("• Set up development environment")
                    elif i == 1:
                        st.write("• Complete pilot development")
                        st.write("• Conduct initial testing")
                        st.write("• Gather stakeholder feedback")
                    else:
                        st.write("• Begin requirements gathering")
                        st.write("• Identify data sources")
                        st.write("• Plan resource allocation")
        
        # Success metrics and KPIs
        st.subheader("Success Metrics and KPIs")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("**Portfolio-Level Metrics:**")
            st.write("• Number of initiatives in production")
            st.write("• Cumulative ROI across all initiatives")
            st.write("• Time to market for new initiatives")
            st.write("• Stakeholder satisfaction scores")
            st.write("• AI capability maturity score")
        
        with col2:
            st.write("**Initiative-Level Metrics:**")
            all_metrics = []
            for initiative in st.session_state.initiatives:
                if initiative.get('primary_metric'):
                    all_metrics.append(initiative['primary_metric'])
            
            for metric in set(all_metrics):
                st.write(f"• {metric}")
        
        # Export action plan
        if st.button("Export Action Plan as Report"):
            # Create a comprehensive report
            report_data = {
                "generated_date": datetime.now().strftime("%Y-%m-%d %H:%M"),
                "total_initiatives": total_initiatives,
                "high_impact_initiatives": high_impact_initiatives,
                "total_investment": total_investment,
                "average_roi": avg_roi,
                "initiatives": sorted_initiatives,
                "stakeholders": st.session_state.stakeholders
            }
            
            # Convert to downloadable format
            import json
            report_json = json.dumps(report_data, indent=2, default=str)
            
            st.download_button(
                label="Download Action Plan (JSON)",
                data=report_json,
                file_name=f"ai_strategy_action_plan_{datetime.now().strftime('%Y%m%d')}.json",
                mime="application/json"
            )
            
            st.success("Action plan generated! Download the file for detailed implementation guidance.")
        
        st.markdown("---")
        st.markdown("### Congratulations!")
        st.markdown("You've completed the AI Strategy Mapping process. Use the insights and action plan to guide your AI transformation journey.")
        show_navigation_buttons()

# Professional Footer
st.markdown("---")
st.markdown("""
<div style="background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%); padding: 2rem; border-radius: 10px; margin-top: 2rem;">
    <div style="text-align: center;">
        <h4 style="color: #667eea; margin-bottom: 1rem;">AI Strategy Mapper</h4>
        <p style="margin-bottom: 1rem; color: #6c757d;">
            <strong>Chapter 3 Tool from AI Playbook for Organisations</strong> • Strategic AI Planning Framework
        </p>
        
        <!-- Book and Toolkit Links -->
        <div style="margin: 1.5rem 0; padding: 1rem; background: rgba(102, 126, 234, 0.1); border-radius: 8px;">
            <h5 style="color: #667eea; margin-bottom: 0.5rem;">📚 AI Playbook for Organisations Toolkit</h5>
            <p style="margin: 0.5rem 0; font-size: 0.9rem; color: #6c757d;">
                <strong>Ch2:</strong> <a href="https://aiready.streamlit.app/" target="_blank" style="color: #667eea; text-decoration: none;">AI Readiness Assessment</a> • 
                <strong>Ch3:</strong> AI Strategy Mapper (this tool)
            </p>
            <p style="margin: 0; font-size: 0.9rem; color: #6c757d;">
                📖 Read the book: <a href="https://medium.com/ai-playbook-for-organisations" target="_blank" style="color: #667eea; text-decoration: none;">AI Playbook for Organisations</a>
            </p>
        </div>
        
        <p style="margin: 0; font-size: 0.8rem; color: #6c757d;">
            Based on: <a href="https://mkonda007.medium.com/ch3-aligning-ai-strategy-with-business-objectives-d4631681053d" 
            target="_blank" style="color: #667eea; text-decoration: none;">Chapter 3: Aligning AI Strategy with Business Objectives</a>
        </p>
    </div>
</div>
""", unsafe_allow_html=True)
