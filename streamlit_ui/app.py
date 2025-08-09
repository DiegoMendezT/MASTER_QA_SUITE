"""
Streamlit UI for MASTER QA SUITE v2.0
Test execution dashboard and monitoring
"""
import streamlit as st
import subprocess
import os
import yaml
from datetime import datetime
import glob

# Page configuration
st.set_page_config(
    page_title="MASTER QA SUITE v2.0",
    page_icon="🧪",
    layout="wide"
)

def load_config():
    """Load configuration from settings.yaml"""
    config_path = os.path.join(os.path.dirname(__file__), '..', 'config', 'settings.yaml')
    with open(config_path, 'r') as file:
        return yaml.safe_load(file)

def get_test_files():
    """Get list of available test files"""
    test_dir = os.path.join(os.path.dirname(__file__), '..', 'tests')
    test_files = glob.glob(os.path.join(test_dir, 'test_*.py'))
    return [os.path.basename(f) for f in test_files]

def run_tests(test_file=None, browser="chrome", parallel=False, markers=None):
    """Execute pytest with specified parameters"""
    cmd = ["python", "-m", "pytest"]
    
    if test_file and test_file != "All Tests":
        cmd.append(f"tests/{test_file}")
    else:
        cmd.append("tests/")
    
    # Add browser selection (if we implement parameterization)
    if markers:
        cmd.extend(["-m", markers])
    
    if parallel:
        cmd.extend(["-n", "auto"])
    
    cmd.extend(["-v", "--tb=short"])
    
    return cmd

def main():
    """Main Streamlit application"""
    
    # Header
    st.title("🧪 MASTER QA SUITE v2.0")
    st.subheader("Selenium Test Execution Dashboard")
    
    # Sidebar configuration
    st.sidebar.header("Test Configuration")
    
    # Load configuration
    try:
        config = load_config()
        st.sidebar.success("✅ Configuration loaded")
    except Exception as e:
        st.sidebar.error(f"❌ Config error: {e}")
        return
    
    # Test selection
    test_files = get_test_files()
    selected_test = st.sidebar.selectbox(
        "Select Test Suite:",
        ["All Tests"] + test_files
    )
    
    # Browser selection
    browser = st.sidebar.selectbox(
        "Select Browser:",
        ["chrome", "firefox", "edge"]
    )
    
    # Test markers
    markers = st.sidebar.selectbox(
        "Test Markers:",
        ["None", "smoke", "regression", "ui", "slow"]
    )
    
    # Parallel execution
    parallel = st.sidebar.checkbox("Parallel Execution", value=False)
    
    # Main content area
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.header("Test Execution")
        
        if st.button("🚀 Run Tests", type="primary"):
            with st.spinner("Running tests..."):
                try:
                    cmd = run_tests(
                        test_file=selected_test if selected_test != "All Tests" else None,
                        browser=browser,
                        parallel=parallel,
                        markers=markers if markers != "None" else None
                    )
                    
                    st.code(" ".join(cmd))
                    
                    # Execute command
                    result = subprocess.run(
                        cmd,
                        capture_output=True,
                        text=True,
                        cwd=os.path.dirname(os.path.dirname(__file__))
                    )
                    
                    # Display results
                    if result.returncode == 0:
                        st.success("✅ Tests completed successfully!")
                    else:
                        st.error("❌ Tests failed!")
                    
                    # Output
                    if result.stdout:
                        st.subheader("Test Output:")
                        st.text_area("STDOUT", result.stdout, height=300)
                    
                    if result.stderr:
                        st.subheader("Errors:")
                        st.text_area("STDERR", result.stderr, height=150)
                        
                except Exception as e:
                    st.error(f"Execution error: {e}")
    
    with col2:
        st.header("Test Status")
        
        # Project info
        st.info(f"""
        **Environment:** {config.get('environment', 'local')}
        **Base URL:** {config.get('base_url', 'N/A')}
        **Implicit Wait:** {config['selenium']['implicit_wait']}s
        **Selected Test:** {selected_test}
        **Browser:** {browser.title()}
        **Parallel:** {'Yes' if parallel else 'No'}
        """)
        
        # Test files info
        st.subheader("Available Tests:")
        for test_file in test_files:
            st.text(f"📄 {test_file}")
        
        # Reports section
        st.subheader("Recent Reports:")
        reports_dir = os.path.join(os.path.dirname(__file__), '..', 'reports')
        
        if os.path.exists(reports_dir):
            report_files = glob.glob(os.path.join(reports_dir, '*.html'))
            
            if report_files:
                latest_report = max(report_files, key=os.path.getctime)
                report_name = os.path.basename(latest_report)
                st.text(f"📊 {report_name}")
                
                if st.button("📱 Open Latest Report"):
                    st.info(f"Report location: {latest_report}")
            else:
                st.text("No reports found")
        
        # Screenshots section
        st.subheader("Recent Screenshots:")
        screenshots_dir = os.path.join(reports_dir, 'screenshots')
        
        if os.path.exists(screenshots_dir):
            screenshots = glob.glob(os.path.join(screenshots_dir, '*.png'))
            
            if screenshots:
                latest_screenshot = max(screenshots, key=os.path.getctime)
                screenshot_name = os.path.basename(latest_screenshot)
                st.text(f"📸 {screenshot_name}")
            else:
                st.text("No screenshots found")

if __name__ == "__main__":
    main()
