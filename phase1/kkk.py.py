import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

st.set_page_config(page_title="Hydrogen Peroxide Market Analysis", layout="wide")

st.title("🚀 Hydrogen Peroxide Global Market Analysis Dashboard")
st.markdown(" Dynamic Analytics Platform")
st.write("---")

@st.cache_data
def load_data():
    df = pd.read_csv('Py Project.csv', encoding='unicode_escape')
    df.columns = df.columns.str.strip()
    return df

try:
    df = load_data()
    
    regions_list = ["All Regions"] + list(df['Region'].unique())
    selected_region = st.selectbox("🌍 Filter Dashboard by Region:", regions_list)
    
    if selected_region != "All Regions":
        filtered_df = df[df['Region'] == selected_region]
    else:
        filtered_df = df
        
    st.subheader("📊 SECTION 1: Global Market Size Overview")
    
    total_market_size = filtered_df['Value imported in 2024 (USD thousand)'].sum()
    avg_hhi = filtered_df['Concentration of supplying countries'].mean()
    
    col_kpi1, col_kpi2 = st.columns(2)
    with col_kpi1:
        st.metric(label=f"Total Market Size ({selected_region})", value=f"${total_market_size:,.0f}K USD")
    with col_kpi2:
        st.metric(label=f"Average Market HHI Index ({selected_region})", value=f"{avg_hhi:.3f}")
        
    st.write("---")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### Q1: Global Market Size Distribution")
        region_data = filtered_df.groupby('Region')['Value imported in 2024 (USD thousand)'].sum().reset_index()
        fig_q1 = px.pie(
            region_data, values='Value imported in 2024 (USD thousand)', names='Region',
            hole=0.6, color_discrete_sequence=px.colors.qualitative.Pastel
        )
        fig_q1.update_layout(margin=dict(t=20, b=20, l=20, r=20), height=350)
        st.plotly_chart(fig_q1, use_container_width=True)

    with col2:
        st.markdown("#### Q2: Top 5 Largest Import Markets")
        top_5_importers = filtered_df.nlargest(5, 'Value imported in 2024 (USD thousand)')
        
        with st.expander("Show Pivot Table for Q2"):
            st.dataframe(top_5_importers[['Importers', 'Value imported in 2024 (USD thousand)']])
            
        fig_q2 = px.bar(
            top_5_importers, x='Value imported in 2024 (USD thousand)', y='Importers',
            orientation='h', color='Value imported in 2024 (USD thousand)',
            color_continuous_scale='Mint', text_auto='.2s'
        )
        fig_q2.update_layout(margin=dict(t=20, b=20, l=20, r=20), height=350, showlegend=False, coloraxis_showscale=False)
        fig_q2.update_yaxes(categoryorder='total ascending')
        st.plotly_chart(fig_q2, use_container_width=True)

    st.write("---")
    
    st.subheader("📈 SECTION 2: Market Growth & Demand Trends")
    col3, col4 = st.columns(2)
    
    with col3:
        st.markdown("#### Q3: Global Import Trends (Value vs Quantity)")
        
        pivot_trend = filtered_df.pivot_table(
            index='Region',
            values=['Annual growth in value between 2020-2024 (%)', 'Annual growth in quantity between 2020-2024 (%)'],
            aggfunc='mean'
        ).reset_index()
        
        with st.expander("Show Growth Pivot Table"):
            st.dataframe(pivot_trend)
            
        if not pivot_trend.empty:
            melted_pivot = pd.melt(pivot_trend, id_vars=['Region'], var_name='Metric', value_name='Rate')
            melted_pivot['Metric'] = melted_pivot['Metric'].replace({
                'Annual growth in value between 2020-2024 (%)': 'Value Growth',
                'Annual growth in quantity between 2020-2024 (%)': 'Quantity Growth'
            })
            
            fig_q3 = px.bar(melted_pivot, x='Region', y='Rate', color='Metric', barmode='group',
                            color_discrete_sequence=['#1e3d59', '#ff6e40'])
            fig_q3.update_layout(margin=dict(t=20, b=20, l=20, r=20), height=350)
            st.plotly_chart(fig_q3, use_container_width=True)
        else:
            st.info("No region data available for the current selection.")

    with col4:
        st.markdown("#### Q4: Top 5 Markets with Strongest Demand Growth")
        top_growth = filtered_df.nlargest(5, 'Annual growth in value between 2020-2024 (%)')
        
        fig_q4 = px.bar(
            top_growth, x='Annual growth in value between 2020-2024 (%)', y='Importers',
            orientation='h', color='Annual growth in value between 2020-2024 (%)',
            color_continuous_scale='Sunsetdark', text_auto='.1f'
        )
        fig_q4.update_layout(margin=dict(t=20, b=20, l=20, r=20), height=350, coloraxis_showscale=False)
        fig_q4.update_yaxes(categoryorder='total ascending')
        st.plotly_chart(fig_q4, use_container_width=True)

    st.write("---")
    
    st.subheader("🎯 SECTION 3: Market Stability & Supply Risk Analysis")
    col5, col6 = st.columns([1, 2])
    
    with col5:
        st.markdown("#### Q5: Global Supply Risk Level (HHI)")
        fig_q5 = go.Figure(go.Indicator(
            mode = "gauge+number",
            value = avg_hhi,
            title = {'text': "HHI Risk Gauge", 'font': {'size': 14}},
            gauge = {
                'axis': {'range': [0, 1]},
                'bar': {'color': "#1e3d59"},
                'steps': [
                    {'range': [0, 0.3], 'color': '#a3e4d7'},
                    {'range': [0.3, 0.6], 'color': '#f8c471'},
                    {'range': [0.6, 1.0], 'color': '#f1948a'}
                ]
            }
        ))
        fig_q5.update_layout(margin=dict(t=40, b=20, l=20, r=20), height=300)
        st.plotly_chart(fig_q5, use_container_width=True)
        
    with col6:
        st.markdown("#### Concentration Index Pivot by Region")
        pivot_concentration = filtered_df.pivot_table(
            index='Region', values='Concentration of supplying countries', aggfunc='mean'
        ).sort_values(by='Concentration of supplying countries', ascending=False)
        
        st.dataframe(pivot_concentration, use_container_width=True)

except FileNotFoundError:
    st.error("❌ ملف 'Py Project.csv' مش موجود في نفس الفولدر! تأكدي من مكانه.")



    with col2:
        st.markdown("#### Q2: Top 5 Largest Import Markets")
        top_5_importers = df.nlargest(5, 'Value imported in 2024 (USD thousand)')


        with st.expander("Show Pivot Table for Q2"):
            st.dataframe(top_5_importers[['Importers', 'Value imported in 2024 (USD thousand)']])

        fig_q2 = px.bar(
            top_5_importers, x='Value imported in 2024 (USD thousand)', y='Importers',
            orientation='h', color='Value imported in 2024 (USD thousand)',
            color_continuous_scale='Mint', text_auto='.2s'
        )
        fig_q2.update_layout(margin=dict(t=20, b=20, l=20, r=20), height=350, showlegend=False, coloraxis_showscale=False)
        fig_q2.update_yaxes(categoryorder='total ascending')
        st.plotly_chart(fig_q2, use_container_width=True)

    st.write("---")

    # ----------------------------------------------------
    st.subheader("📈 SECTION 2: Market Growth & Demand Trends")
    col3, col4 = st.columns(2)

    # Question 3: Pivot Table & Grouped Bar Chart
    with col3:
        st.markdown("#### Q3: Global Import Trends (Value vs Quantity)")


        pivot_trend = df.pivot_table(
            index='Region',
            values=['Annual growth in value between 2020-2024 (%)', 'Annual growth in quantity between 2020-2024 (%)'],
            aggfunc='mean'
        ).reset_index()

        with st.expander("Show Growth Pivot Table"):
            st.dataframe(pivot_trend)

        melted_pivot = pd.melt(pivot_trend, id_vars=['Region'], var_name='Metric', value_name='Rate')
        melted_pivot['Metric'] = melted_pivot['Metric'].replace({
            'Annual growth in value between 2020-2024 (%)': 'Value Growth',
            'Annual growth in quantity between 2020-2024 (%)': 'Quantity Growth'
        })

        fig_q3 = px.bar(melted_pivot, x='Region', y='Rate', color='Metric', barmode='group',
                        color_discrete_sequence=['#1e3d59', '#ff6e40'])
        fig_q3.update_layout(margin=dict(t=20, b=20, l=20, r=20), height=350)
        st.plotly_chart(fig_q3, use_container_width=True)


    with col4:
        st.markdown("#### Q4: Top 5 Markets with Strongest Demand Growth")
        top_growth = df.nlargest(5, 'Annual growth in value between 2020-2024 (%)')

        fig_q4 = px.bar(
            top_growth, x='Annual growth in value between 2020-2024 (%)', y='Importers',
            orientation='h', color='Annual growth in value between 2020-2024 (%)',
            color_continuous_scale='Sunsetdark', text_auto='.1f'
        )
        fig_q4.update_layout(margin=dict(t=20, b=20, l=20, r=20), height=350, coloraxis_showscale=False)
        fig_q4.update_yaxes(categoryorder='total ascending')
        st.plotly_chart(fig_q4, use_container_width=True)

    st.write("---")



    # ----------------------------------------------------
    st.subheader("🎯 SECTION 3: Market Stability & Supply Risk Analysis")
    col5, col6 = st.columns([1, 2])

    with col5:
        st.markdown("#### Q5: Global Supply Risk Level (HHI)")
        fig_q5 = go.Figure(go.Indicator(
            mode = "gauge+number",
            value = avg_hhi,
            title = {'text': "HHI Risk Gauge", 'font': {'size': 14}},
            gauge = {
                'axis': {'range': [0, 1]},
                'bar': {'color': "#1e3d59"},
                'steps': [
                    {'range': [0, 0.3], 'color': '#a3e4d7'},
                    {'range': [0.3, 0.6], 'color': '#f8c471'},
                    {'range': [0.6, 1.0], 'color': '#f1948a'}
                ]
            }
        ))
        fig_q5.update_layout(margin=dict(t=40, b=20, l=20, r=20), height=300)
        st.plotly_chart(fig_q5, use_container_width=True)

    with col6:
        st.markdown("#### Concentration Index Pivot by Region")
        pivot_concentration = df.pivot_table(
            index='Region', values='Concentration of supplying countries', aggfunc='mean'
        ).sort_values(by='Concentration of supplying countries', ascending=False)

        st.dataframe(pivot_concentration, use_container_width=True)

except FileNotFoundError:
    st.error("❌ ملف 'Py Project.csv' لم يتم العثور عليه فالفولدر! تأكدي من مكانه.")