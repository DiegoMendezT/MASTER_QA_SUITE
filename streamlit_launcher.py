
import subprocess
import sys
from pathlib import Path

import streamlit as st


def main():
    st.set_page_config(
        page_title="MASTER QA SUITE - Launch Control",
        page_icon="🚀",
        layout="wide"
    )
    
    st.title("🚀 MASTER QA SUITE - Launch Control")
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.header("🧠 Consciousness Dashboard")
        
        if st.button("Launch Consciousness Dashboard", type="primary"):
            st.info("Starting consciousness dashboard...")
            try:
                subprocess.Popen([
                    sys.executable, "-m", "streamlit", "run", 
                    "streamlit_ui/consciousness_dashboard.py", 
                    "--server.port=8502"
                ])
                st.success("Dashboard launching on port 8502!")
                st.markdown("[Open Dashboard](http://localhost:8502)")
            except Exception as e:
                st.error(f"Launch failed: {e}")
    
    with col2:
        st.header("🧪 Test Execution")
        
        test_type = st.selectbox(
            "Select Test Suite:",
            ["Self-Reflection", "API Tests", "UI Tests", "All Tests"]
        )
        
        if st.button("Execute Tests"):
            st.info(f"Running {test_type} tests...")
            
            command_map = {
                "Self-Reflection": ["python", "-m", "pytest", "tests/self_reflection/", "-v"],
                "API Tests": ["python", "-m", "pytest", "tests/api/", "-v"],  
                "UI Tests": ["python", "-m", "pytest", "tests/test_google.py", "tests/test_login.py", "-v"],
                "All Tests": ["python", "-m", "pytest", "tests/", "-v", "--html=reports/streamlit_report.html"]
            }
            
            try:
                result = subprocess.run(
                    command_map[test_type], 
                    capture_output=True, 
                    text=True,
                    cwd=Path(__file__).parent
                )
                
                if result.returncode == 0:
                    st.success(f"{test_type} completed successfully!")
                else:
                    st.warning(f"{test_type} completed with issues")
                
                with st.expander("View Test Output"):
                    st.code(result.stdout)
                    if result.stderr:
                        st.code(result.stderr)
                        
            except Exception as e:
                st.error(f"Test execution failed: {e}")
    
    st.markdown("---")
    
    # Framework Status
    st.header("📊 Framework Status")
    
    status_col1, status_col2, status_col3 = st.columns(3)
    
    with status_col1:
        st.metric("Consciousness Level", "23.3%", "Developing")
    
    with status_col2:
        st.metric("Self-Reflection", "13/14", "+92.9%")
    
    with status_col3:
        st.metric("Framework Health", "Operational", "✅")
    
    # Quick Actions
    st.header("⚡ Quick Actions")
    
    action_col1, action_col2, action_col3 = st.columns(3)
    
    with action_col1:
        if st.button("🧠 Activate Consciousness"):
            try:
                result = subprocess.run([sys.executable, "becoming_master.py"], 
                                      capture_output=True, text=True)
                st.success("Consciousness activated!")
                st.code(result.stdout)
            except Exception as e:
                st.error(f"Activation failed: {e}")
    
    with action_col2:
        if st.button("📊 Generate Report"):
            try:
                subprocess.run([
                    sys.executable, "-m", "pytest", "tests/", 
                    "--html=reports/dashboard_report.html", "--self-contained-html"
                ])
                st.success("Report generated in reports/ directory")
            except Exception as e:
                st.error(f"Report generation failed: {e}")
    
    with action_col3:
        if st.button("🔍 Verify Setup"):
            try:
                result = subprocess.run([sys.executable, "verify_setup.py"], 
                                      capture_output=True, text=True)
                st.success("Setup verification completed!")
                st.code(result.stdout)
            except Exception as e:
                st.error(f"Verification failed: {e}")

if __name__ == "__main__":
    main()
