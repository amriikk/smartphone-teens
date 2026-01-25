"""
Data Quality Report Generator
=============================
A comprehensive tool for analyzing CSV datasets and identifying:
- Missing values (with heatmap visualization)
- Outliers (with boxplot visualization)
- Duplicate rows

Usage:
    python data_quality_report.py <path_to_csv>
    
Output:
    - Console summary report
    - data_quality_report.html (detailed HTML report with visualizations)
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
import sys
import warnings
from datetime import datetime
import base64
from io import BytesIO

warnings.filterwarnings('ignore')

# Set style for visualizations
plt.style.use('seaborn-v0_8-whitegrid')
sns.set_palette("husl")


class DataQualityReport:
    """Generate comprehensive data quality reports for CSV datasets."""
    
    def __init__(self, filepath: str):
        """Initialize with path to CSV file."""
        self.filepath = Path(filepath)
        self.df = None
        self.report_data = {}
        
    def load_data(self) -> bool:
        """Load the CSV file into a DataFrame."""
        try:
            self.df = pd.read_csv(self.filepath)
            self.report_data['filename'] = self.filepath.name
            self.report_data['rows'] = len(self.df)
            self.report_data['columns'] = len(self.df.columns)
            self.report_data['column_names'] = list(self.df.columns)
            print(f"✓ Loaded '{self.filepath.name}' successfully")
            print(f"  Shape: {self.df.shape[0]:,} rows × {self.df.shape[1]} columns\n")
            return True
        except Exception as e:
            print(f"✗ Error loading file: {e}")
            return False
    
    # =========================================================================
    # MISSING VALUES ANALYSIS
    # =========================================================================
    
    def analyze_missing_values(self) -> dict:
        """Analyze missing values in the dataset."""
        print("=" * 60)
        print("MISSING VALUES ANALYSIS")
        print("=" * 60)
        
        missing = self.df.isnull().sum()
        missing_pct = (missing / len(self.df)) * 100
        
        missing_df = pd.DataFrame({
            'Column': self.df.columns,
            'Missing Count': missing.values,
            'Missing %': missing_pct.values,
            'Data Type': self.df.dtypes.values
        }).sort_values('Missing %', ascending=False)
        
        # Classify missing pattern
        total_missing = missing.sum()
        total_cells = self.df.shape[0] * self.df.shape[1]
        overall_missing_pct = (total_missing / total_cells) * 100
        
        # Columns with >50% missing (potentially useless)
        high_missing_cols = missing_df[missing_df['Missing %'] > 50]['Column'].tolist()
        
        # Columns with any missing
        cols_with_missing = missing_df[missing_df['Missing %'] > 0]
        
        self.report_data['missing'] = {
            'total_missing_cells': int(total_missing),
            'total_cells': int(total_cells),
            'overall_missing_pct': round(overall_missing_pct, 2),
            'columns_with_missing': len(cols_with_missing),
            'high_missing_columns': high_missing_cols,
            'details': missing_df.to_dict('records')
        }
        
        # Print summary
        print(f"\n📊 Overall: {total_missing:,} missing values ({overall_missing_pct:.2f}% of all data)")
        print(f"   Columns with missing data: {len(cols_with_missing)} of {len(self.df.columns)}")
        
        if len(high_missing_cols) > 0:
            print(f"\n⚠️  High-risk columns (>50% missing):")
            for col in high_missing_cols:
                pct = missing_pct[col]
                print(f"   - {col}: {pct:.1f}% missing")
        
        if len(cols_with_missing) > 0:
            print(f"\n📋 Missing Values by Column:")
            print("-" * 50)
            for _, row in cols_with_missing.iterrows():
                if row['Missing %'] > 0:
                    bar = "█" * int(row['Missing %'] / 5) + "░" * (20 - int(row['Missing %'] / 5))
                    print(f"   {row['Column'][:25]:<25} {bar} {row['Missing %']:>6.1f}%")
        else:
            print("\n✅ No missing values found!")
        
        return self.report_data['missing']
    
    def create_missing_heatmap(self) -> str:
        """Create a heatmap visualization of missing values."""
        fig, axes = plt.subplots(1, 2, figsize=(14, max(6, len(self.df.columns) * 0.3)))
        
        # Heatmap of missing values (sample if too large)
        sample_size = min(100, len(self.df))
        sample_df = self.df.sample(n=sample_size, random_state=42) if len(self.df) > 100 else self.df
        
        ax1 = axes[0]
        sns.heatmap(sample_df.isnull(), cbar=True, yticklabels=False, 
                    cmap='YlOrRd', ax=ax1)
        ax1.set_title(f'Missing Values Heatmap\n(Sample of {sample_size} rows)', fontsize=12, fontweight='bold')
        ax1.set_xlabel('Columns')
        ax1.set_ylabel('Rows')
        plt.setp(ax1.xaxis.get_majorticklabels(), rotation=45, ha='right')
        
        # Bar chart of missing percentages
        ax2 = axes[1]
        missing_pct = (self.df.isnull().sum() / len(self.df)) * 100
        colors = ['#e74c3c' if x > 50 else '#f39c12' if x > 20 else '#3498db' for x in missing_pct]
        
        bars = ax2.barh(range(len(missing_pct)), missing_pct.values, color=colors)
        ax2.set_yticks(range(len(missing_pct)))
        ax2.set_yticklabels(missing_pct.index)
        ax2.set_xlabel('Missing %')
        ax2.set_title('Missing Values by Column', fontsize=12, fontweight='bold')
        ax2.axvline(x=50, color='red', linestyle='--', alpha=0.5, label='50% threshold')
        ax2.legend()
        
        # Add percentage labels
        for i, (bar, pct) in enumerate(zip(bars, missing_pct.values)):
            if pct > 0:
                ax2.text(pct + 1, i, f'{pct:.1f}%', va='center', fontsize=8)
        
        plt.tight_layout()
        
        # Convert to base64 for HTML embedding
        buffer = BytesIO()
        plt.savefig(buffer, format='png', dpi=150, bbox_inches='tight')
        buffer.seek(0)
        img_str = base64.b64encode(buffer.read()).decode()
        plt.close()
        
        return img_str
    
    # =========================================================================
    # OUTLIER ANALYSIS
    # =========================================================================
    
    def analyze_outliers(self) -> dict:
        """Analyze outliers in numeric columns using IQR method."""
        print("\n" + "=" * 60)
        print("OUTLIER ANALYSIS")
        print("=" * 60)
        
        numeric_cols = self.df.select_dtypes(include=[np.number]).columns.tolist()
        
        if not numeric_cols:
            print("\n⚠️  No numeric columns found for outlier analysis.")
            self.report_data['outliers'] = {'numeric_columns': 0, 'details': []}
            return self.report_data['outliers']
        
        outlier_details = []
        
        print(f"\n📊 Analyzing {len(numeric_cols)} numeric columns...")
        print("-" * 60)
        
        for col in numeric_cols:
            data = self.df[col].dropna()
            
            if len(data) == 0:
                continue
                
            Q1 = data.quantile(0.25)
            Q3 = data.quantile(0.75)
            IQR = Q3 - Q1
            
            lower_bound = Q1 - 1.5 * IQR
            upper_bound = Q3 + 1.5 * IQR
            
            outliers = data[(data < lower_bound) | (data > upper_bound)]
            outlier_count = len(outliers)
            outlier_pct = (outlier_count / len(data)) * 100
            
            # Check for "impossible" values
            impossible_values = []
            if data.min() < 0 and col.lower() in ['age', 'price', 'quantity', 'count', 'amount']:
                impossible_values.append(f"Negative values found (min: {data.min():.2f})")
            if col.lower() == 'age' and data.max() > 120:
                impossible_values.append(f"Age > 120 found (max: {data.max():.0f})")
            
            detail = {
                'column': col,
                'count': len(data),
                'mean': round(data.mean(), 2),
                'std': round(data.std(), 2),
                'min': round(data.min(), 2),
                'max': round(data.max(), 2),
                'Q1': round(Q1, 2),
                'Q3': round(Q3, 2),
                'IQR': round(IQR, 2),
                'lower_bound': round(lower_bound, 2),
                'upper_bound': round(upper_bound, 2),
                'outlier_count': outlier_count,
                'outlier_pct': round(outlier_pct, 2),
                'impossible_values': impossible_values
            }
            outlier_details.append(detail)
            
            # Print summary
            status = "⚠️ " if outlier_pct > 5 or impossible_values else "  "
            print(f"{status}{col[:30]:<30} | Outliers: {outlier_count:>6} ({outlier_pct:>5.1f}%) | Range: [{data.min():.2f}, {data.max():.2f}]")
            
            for warning in impossible_values:
                print(f"      🚨 {warning}")
        
        # Summary statistics
        total_outliers = sum(d['outlier_count'] for d in outlier_details)
        cols_with_outliers = sum(1 for d in outlier_details if d['outlier_count'] > 0)
        
        self.report_data['outliers'] = {
            'numeric_columns': len(numeric_cols),
            'columns_with_outliers': cols_with_outliers,
            'total_outliers': total_outliers,
            'details': outlier_details
        }
        
        print(f"\n📈 Summary: {total_outliers:,} total outliers across {cols_with_outliers} columns")
        
        return self.report_data['outliers']
    
    def create_outlier_boxplots(self) -> str:
        """Create boxplots for numeric columns to visualize outliers."""
        numeric_cols = self.df.select_dtypes(include=[np.number]).columns.tolist()

        if not numeric_cols:
            return ""

        # Include all numeric columns
        plot_cols = numeric_cols
        n_cols = len(plot_cols)

        # Calculate grid dimensions (3 columns per row)
        n_rows = (n_cols + 2) // 3

        fig, axes = plt.subplots(n_rows, 3, figsize=(14, 4 * n_rows))
        axes = axes.flatten() if n_cols > 1 else [axes]

        for idx, col in enumerate(plot_cols):
            ax = axes[idx]
            data = self.df[col].dropna()
            
            # Create boxplot
            bp = ax.boxplot(data, patch_artist=True, vert=True)
            bp['boxes'][0].set_facecolor('#3498db')
            bp['boxes'][0].set_alpha(0.7)
            
            # Color outliers red
            for flier in bp['fliers']:
                flier.set(marker='o', color='#e74c3c', alpha=0.5, markersize=5)
            
            ax.set_title(f'{col[:25]}', fontsize=10, fontweight='bold')
            ax.set_ylabel('Value')
            
            # Add stats annotation
            Q1 = data.quantile(0.25)
            Q3 = data.quantile(0.75)
            IQR = Q3 - Q1
            outlier_count = len(data[(data < Q1 - 1.5*IQR) | (data > Q3 + 1.5*IQR)])
            
            stats_text = f'n={len(data):,}\nOutliers: {outlier_count}'
            ax.text(0.98, 0.98, stats_text, transform=ax.transAxes, 
                    fontsize=8, verticalalignment='top', horizontalalignment='right',
                    bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))
        
        # Hide unused subplots
        for idx in range(len(plot_cols), len(axes)):
            axes[idx].set_visible(False)
        
        plt.suptitle('Outlier Detection: Boxplots of Numeric Columns', 
                     fontsize=14, fontweight='bold', y=1.02)
        plt.tight_layout()
        
        # Convert to base64
        buffer = BytesIO()
        plt.savefig(buffer, format='png', dpi=150, bbox_inches='tight')
        buffer.seek(0)
        img_str = base64.b64encode(buffer.read()).decode()
        plt.close()
        
        return img_str
    
    # =========================================================================
    # DUPLICATE ANALYSIS
    # =========================================================================
    
    def analyze_duplicates(self) -> dict:
        """Analyze duplicate rows in the dataset."""
        print("\n" + "=" * 60)
        print("DUPLICATE ANALYSIS")
        print("=" * 60)
        
        # Exact duplicates
        exact_duplicates = self.df.duplicated().sum()
        exact_dup_pct = (exact_duplicates / len(self.df)) * 100
        
        # Get examples of duplicates
        dup_examples = []
        if exact_duplicates > 0:
            dup_mask = self.df.duplicated(keep=False)
            dup_df = self.df[dup_mask].head(10)
            dup_examples = dup_df.to_dict('records')
        
        # Check for near-duplicates on key columns (if identifiable)
        potential_key_cols = []
        for col in self.df.columns:
            col_lower = col.lower()
            if any(key in col_lower for key in ['id', 'key', 'code', 'number', 'email']):
                potential_key_cols.append(col)
        
        key_col_duplicates = {}
        for col in potential_key_cols[:5]:  # Limit to 5 potential key columns
            dup_count = self.df[col].duplicated().sum()
            if dup_count > 0:
                key_col_duplicates[col] = dup_count
        
        self.report_data['duplicates'] = {
            'exact_duplicates': int(exact_duplicates),
            'exact_duplicate_pct': round(exact_dup_pct, 2),
            'potential_key_columns': potential_key_cols,
            'key_column_duplicates': key_col_duplicates,
            'examples': dup_examples[:5]
        }
        
        # Print summary
        print(f"\n📊 Exact Duplicate Rows: {exact_duplicates:,} ({exact_dup_pct:.2f}%)")
        
        if exact_duplicates > 0:
            print(f"   ⚠️  These rows will bias your model if not removed!")
        else:
            print("   ✅ No exact duplicate rows found")
        
        if key_col_duplicates:
            print(f"\n📋 Potential Key Column Duplicates:")
            for col, count in key_col_duplicates.items():
                print(f"   - {col}: {count:,} duplicates")
        
        return self.report_data['duplicates']
    
    # =========================================================================
    # DATA TYPE ANALYSIS
    # =========================================================================
    
    def analyze_data_types(self) -> dict:
        """Analyze data types and potential type mismatches."""
        print("\n" + "=" * 60)
        print("DATA TYPE ANALYSIS")
        print("=" * 60)
        
        type_summary = self.df.dtypes.value_counts().to_dict()
        type_summary = {str(k): v for k, v in type_summary.items()}
        
        column_types = []
        type_warnings = []
        
        for col in self.df.columns:
            dtype = str(self.df[col].dtype)
            unique_count = self.df[col].nunique()
            unique_pct = (unique_count / len(self.df)) * 100
            
            col_info = {
                'column': col,
                'dtype': dtype,
                'unique_values': unique_count,
                'unique_pct': round(unique_pct, 2)
            }
            column_types.append(col_info)
            
            # Check for potential type issues
            if dtype == 'object':
                # Check if it could be numeric
                try:
                    pd.to_numeric(self.df[col].dropna().head(100), errors='raise')
                    type_warnings.append(f"'{col}' is stored as text but appears numeric")
                except:
                    pass
                
                # Check if it could be datetime
                try:
                    pd.to_datetime(self.df[col].dropna().head(100), errors='raise')
                    type_warnings.append(f"'{col}' is stored as text but appears to be datetime")
                except:
                    pass
        
        self.report_data['data_types'] = {
            'summary': type_summary,
            'column_details': column_types,
            'warnings': type_warnings
        }
        
        # Print summary
        print(f"\n📊 Data Type Distribution:")
        for dtype, count in type_summary.items():
            print(f"   {dtype}: {count} columns")
        
        if type_warnings:
            print(f"\n⚠️  Potential Type Issues:")
            for warning in type_warnings:
                print(f"   - {warning}")
        
        return self.report_data['data_types']

    # =========================================================================
    # CATEGORICAL VALUES ANALYSIS
    # =========================================================================

    def analyze_categorical_values(self) -> dict:
        """Analyze categorical columns and list all unique values."""
        print("\n" + "=" * 60)
        print("CATEGORICAL VALUES ANALYSIS")
        print("=" * 60)

        # Get categorical columns (object and category dtypes only)
        categorical_cols = self.df.select_dtypes(include=['object', 'category']).columns.tolist()

        if not categorical_cols:
            print("\n⚠️  No categorical columns found.")
            self.report_data['categorical'] = {'columns': 0, 'details': []}
            return self.report_data['categorical']

        categorical_details = []

        print(f"\n📊 Analyzing {len(categorical_cols)} categorical columns...")
        print("-" * 60)

        for col in categorical_cols:
            unique_values = self.df[col].dropna().unique().tolist()
            value_counts = self.df[col].value_counts(dropna=False).to_dict()

            detail = {
                'column': col,
                'dtype': str(self.df[col].dtype),
                'unique_count': len(unique_values),
                'unique_values': unique_values,
                'value_counts': value_counts,
                'has_nulls': self.df[col].isnull().any()
            }
            categorical_details.append(detail)

            # Print summary
            print(f"\n   {col} ({len(unique_values)} unique values):")
            for val in unique_values[:10]:  # Show first 10 in console
                count = value_counts.get(val, 0)
                print(f"      - {val}: {count:,}")
            if len(unique_values) > 10:
                print(f"      ... and {len(unique_values) - 10} more values")

        self.report_data['categorical'] = {
            'columns': len(categorical_cols),
            'details': categorical_details
        }

        print(f"\n📈 Summary: {len(categorical_cols)} categorical columns analyzed")

        return self.report_data['categorical']

    # =========================================================================
    # HTML REPORT GENERATION
    # =========================================================================
    
    def generate_html_report(self, output_path: str = None) -> str:
        """Generate a comprehensive HTML report with all visualizations."""
        
        if output_path is None:
            output_path = self.filepath.stem + "_quality_report.html"
        
        # Generate visualizations
        missing_heatmap = self.create_missing_heatmap()
        outlier_boxplots = self.create_outlier_boxplots()
        
        # Build HTML
        html = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Data Quality Report - {self.report_data['filename']}</title>
    <style>
        * {{ box-sizing: border-box; margin: 0; padding: 0; }}
        body {{ 
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; 
            line-height: 1.6; 
            color: #333;
            background: #f5f7fa;
            padding: 20px;
        }}
        .container {{ max-width: 1200px; margin: 0 auto; }}
        .header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 30px;
            border-radius: 10px;
            margin-bottom: 20px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }}
        .header h1 {{ font-size: 2em; margin-bottom: 10px; }}
        .header .meta {{ opacity: 0.9; font-size: 0.95em; }}
        .card {{
            background: white;
            border-radius: 10px;
            padding: 25px;
            margin-bottom: 20px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.08);
        }}
        .card h2 {{
            color: #667eea;
            border-bottom: 2px solid #667eea;
            padding-bottom: 10px;
            margin-bottom: 20px;
        }}
        .stats-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 15px;
            margin-bottom: 20px;
        }}
        .stat-box {{
            background: #f8f9fa;
            padding: 20px;
            border-radius: 8px;
            text-align: center;
            border-left: 4px solid #667eea;
        }}
        .stat-box .number {{ font-size: 2em; font-weight: bold; color: #667eea; }}
        .stat-box .label {{ color: #666; font-size: 0.9em; }}
        .warning {{ color: #e74c3c; }}
        .success {{ color: #27ae60; }}
        table {{
            width: 100%;
            border-collapse: collapse;
            margin: 15px 0;
            font-size: 0.9em;
        }}
        th, td {{
            padding: 12px;
            text-align: left;
            border-bottom: 1px solid #ddd;
        }}
        th {{ background: #f8f9fa; font-weight: 600; }}
        tr:hover {{ background: #f8f9fa; }}
        .visualization {{ text-align: center; margin: 20px 0; }}
        .visualization img {{ max-width: 100%; border-radius: 8px; }}
        .progress-bar {{
            background: #e9ecef;
            border-radius: 10px;
            height: 20px;
            overflow: hidden;
        }}
        .progress-fill {{
            height: 100%;
            background: linear-gradient(90deg, #667eea, #764ba2);
            transition: width 0.3s;
        }}
        .badge {{
            display: inline-block;
            padding: 4px 8px;
            border-radius: 4px;
            font-size: 0.8em;
            font-weight: 600;
        }}
        .badge-danger {{ background: #ffebee; color: #c62828; }}
        .badge-warning {{ background: #fff3e0; color: #ef6c00; }}
        .badge-success {{ background: #e8f5e9; color: #2e7d32; }}
        .summary-section {{
            background: linear-gradient(135deg, #f5f7fa 0%, #e4e8ec 100%);
            padding: 20px;
            border-radius: 8px;
            margin-top: 20px;
        }}
        .footer {{
            text-align: center;
            padding: 20px;
            color: #666;
            font-size: 0.9em;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>📊 Data Quality Report</h1>
            <div class="meta">
                <strong>Dataset:</strong> {self.report_data['filename']} | 
                <strong>Rows:</strong> {self.report_data['rows']:,} | 
                <strong>Columns:</strong> {self.report_data['columns']} |
                <strong>Generated:</strong> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
            </div>
        </div>

        <!-- Executive Summary -->
        <div class="card">
            <h2>📋 Executive Summary</h2>
            <div class="stats-grid">
                <div class="stat-box">
                    <div class="number">{self.report_data['rows']:,}</div>
                    <div class="label">Total Rows</div>
                </div>
                <div class="stat-box">
                    <div class="number">{self.report_data['columns']}</div>
                    <div class="label">Total Columns</div>
                </div>
                <div class="stat-box">
                    <div class="number">{self.report_data['missing']['overall_missing_pct']:.1f}%</div>
                    <div class="label">Missing Data</div>
                </div>
                <div class="stat-box">
                    <div class="number">{self.report_data['duplicates']['exact_duplicates']:,}</div>
                    <div class="label">Duplicate Rows</div>
                </div>
            </div>
        </div>

        <!-- Missing Values -->
        <div class="card">
            <h2>🔍 Missing Values Analysis</h2>
            <div class="stats-grid">
                <div class="stat-box">
                    <div class="number">{self.report_data['missing']['total_missing_cells']:,}</div>
                    <div class="label">Missing Cells</div>
                </div>
                <div class="stat-box">
                    <div class="number">{self.report_data['missing']['columns_with_missing']}</div>
                    <div class="label">Affected Columns</div>
                </div>
                <div class="stat-box">
                    <div class="number">{len(self.report_data['missing']['high_missing_columns'])}</div>
                    <div class="label">High-Risk Columns (&gt;50%)</div>
                </div>
            </div>
            
            <div class="visualization">
                <img src="data:image/png;base64,{missing_heatmap}" alt="Missing Values Heatmap">
            </div>
            
            <h3>Missing Values by Column</h3>
            <table>
                <thead>
                    <tr>
                        <th>Column</th>
                        <th>Missing Count</th>
                        <th>Missing %</th>
                        <th>Status</th>
                    </tr>
                </thead>
                <tbody>
                    {''.join(f"""
                    <tr>
                        <td>{row['Column']}</td>
                        <td>{row['Missing Count']:,}</td>
                        <td>
                            <div class="progress-bar">
                                <div class="progress-fill" style="width: {min(row['Missing %'], 100)}%"></div>
                            </div>
                            {row['Missing %']:.1f}%
                        </td>
                        <td>
                            {'<span class="badge badge-danger">Critical</span>' if row['Missing %'] > 50 
                             else '<span class="badge badge-warning">Warning</span>' if row['Missing %'] > 20 
                             else '<span class="badge badge-success">OK</span>' if row['Missing %'] == 0 
                             else '<span class="badge badge-warning">Minor</span>'}
                        </td>
                    </tr>
                    """ for row in self.report_data['missing']['details'][:20])}
                </tbody>
            </table>
        </div>

        <!-- Outliers -->
        <div class="card">
            <h2>📈 Outlier Analysis</h2>
            <p>Using the IQR (Interquartile Range) method to detect statistical outliers in numeric columns.</p>
            
            <div class="stats-grid">
                <div class="stat-box">
                    <div class="number">{self.report_data['outliers']['numeric_columns']}</div>
                    <div class="label">Numeric Columns</div>
                </div>
                <div class="stat-box">
                    <div class="number">{self.report_data['outliers']['columns_with_outliers']}</div>
                    <div class="label">Columns with Outliers</div>
                </div>
                <div class="stat-box">
                    <div class="number">{self.report_data['outliers']['total_outliers']:,}</div>
                    <div class="label">Total Outliers</div>
                </div>
            </div>
            
            {'<div class="visualization"><img src="data:image/png;base64,' + outlier_boxplots + '" alt="Outlier Boxplots"></div>' if outlier_boxplots else '<p>No numeric columns to analyze.</p>'}
            
            <h3>Outlier Details by Column</h3>
            <table>
                <thead>
                    <tr>
                        <th>Column</th>
                        <th>Min</th>
                        <th>Max</th>
                        <th>Mean</th>
                        <th>Outliers</th>
                        <th>Outlier %</th>
                        <th>Warnings</th>
                    </tr>
                </thead>
                <tbody>
                    {''.join(f"""
                    <tr>
                        <td>{row['column']}</td>
                        <td>{row['min']:,.2f}</td>
                        <td>{row['max']:,.2f}</td>
                        <td>{row['mean']:,.2f}</td>
                        <td>{row['outlier_count']:,}</td>
                        <td>{row['outlier_pct']:.1f}%</td>
                        <td>{'<br>'.join(f'🚨 {w}' for w in row['impossible_values']) if row['impossible_values'] else '✓'}</td>
                    </tr>
                    """ for row in self.report_data['outliers']['details'])}
                </tbody>
            </table>
        </div>

        <!-- Duplicates -->
        <div class="card">
            <h2>🔄 Duplicate Analysis</h2>
            <div class="stats-grid">
                <div class="stat-box">
                    <div class="number {'warning' if self.report_data['duplicates']['exact_duplicates'] > 0 else 'success'}">
                        {self.report_data['duplicates']['exact_duplicates']:,}
                    </div>
                    <div class="label">Exact Duplicate Rows</div>
                </div>
                <div class="stat-box">
                    <div class="number">{self.report_data['duplicates']['exact_duplicate_pct']:.2f}%</div>
                    <div class="label">Percentage of Data</div>
                </div>
            </div>
            
            {f'''
            <div class="summary-section">
                <h4>⚠️ Key Column Duplicates Detected</h4>
                <p>These columns appear to be identifiers but contain duplicate values:</p>
                <ul>
                    {''.join(f"<li><strong>{col}</strong>: {count:,} duplicates</li>" for col, count in self.report_data['duplicates']['key_column_duplicates'].items())}
                </ul>
            </div>
            ''' if self.report_data['duplicates']['key_column_duplicates'] else ''}
            
            {f'''
            <div class="summary-section" style="background: #ffebee;">
                <h4>🚨 Action Required</h4>
                <p>Found <strong>{self.report_data['duplicates']['exact_duplicates']:,}</strong> duplicate rows. 
                These should be investigated and likely removed before model training to prevent bias.</p>
            </div>
            ''' if self.report_data['duplicates']['exact_duplicates'] > 0 else '''
            <div class="summary-section" style="background: #e8f5e9;">
                <h4>✅ No Exact Duplicates</h4>
                <p>Great! No exact duplicate rows were found in the dataset.</p>
            </div>
            '''}
        </div>

        <!-- Categorical Values -->
        <div class="card">
            <h2>📝 Categorical Values Analysis</h2>
            <div class="stats-grid">
                <div class="stat-box">
                    <div class="number">{self.report_data.get('categorical', {}).get('columns', 0)}</div>
                    <div class="label">Categorical Columns</div>
                </div>
            </div>

            {self._generate_categorical_html()}
        </div>

        <!-- Recommendations -->
        <div class="card">
            <h2>💡 Recommendations</h2>
            <div class="summary-section">
                <h4>Data Quality Score</h4>
                {self._generate_quality_score_html()}
            </div>
            
            <h3>Suggested Actions:</h3>
            <ol style="padding-left: 20px; margin-top: 15px;">
                {self._generate_recommendations_html()}
            </ol>
        </div>

        <div class="footer">
            <p>Generated by Data Quality Report Tool | {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
        </div>
    </div>
</body>
</html>
        """
        
        # Save HTML file
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(html)
        
        print(f"\n✅ HTML report saved to: {output_path}")
        return output_path
    
    def _generate_quality_score_html(self) -> str:
        """Generate a data quality score based on the analysis."""
        # Calculate score (0-100)
        score = 100
        
        # Deduct for missing values
        missing_pct = self.report_data['missing']['overall_missing_pct']
        score -= min(30, missing_pct * 0.5)
        
        # Deduct for duplicates
        dup_pct = self.report_data['duplicates']['exact_duplicate_pct']
        score -= min(20, dup_pct * 2)
        
        # Deduct for high outlier columns
        if self.report_data['outliers']['details']:
            high_outlier_cols = sum(1 for d in self.report_data['outliers']['details'] if d['outlier_pct'] > 10)
            score -= min(20, high_outlier_cols * 5)
        
        score = max(0, round(score))
        
        color = '#27ae60' if score >= 80 else '#f39c12' if score >= 60 else '#e74c3c'
        
        return f"""
        <div style="text-align: center; padding: 20px;">
            <div style="font-size: 4em; font-weight: bold; color: {color};">{score}</div>
            <div style="font-size: 1.2em; color: #666;">out of 100</div>
            <div class="progress-bar" style="height: 30px; margin-top: 15px;">
                <div class="progress-fill" style="width: {score}%; background: {color};"></div>
            </div>
            <div style="margin-top: 10px; color: #666;">
                {'Excellent data quality!' if score >= 80 
                 else 'Good quality with some issues to address' if score >= 60 
                 else 'Significant data quality issues detected'}
            </div>
        </div>
        """
    
    def _generate_recommendations_html(self) -> str:
        """Generate recommendations based on the analysis."""
        recommendations = []
        
        # Missing value recommendations
        if self.report_data['missing']['high_missing_columns']:
            cols = ', '.join(self.report_data['missing']['high_missing_columns'][:3])
            recommendations.append(
                f"<li><strong>High Missing Values:</strong> Consider dropping columns with >50% missing data ({cols}...) or investigate why data is missing.</li>"
            )
        
        if self.report_data['missing']['overall_missing_pct'] > 5:
            recommendations.append(
                "<li><strong>Missing Data Strategy:</strong> Implement appropriate imputation (mean/median for numeric, mode for categorical) or use algorithms that handle missing values.</li>"
            )
        
        # Duplicate recommendations
        if self.report_data['duplicates']['exact_duplicates'] > 0:
            recommendations.append(
                f"<li><strong>Remove Duplicates:</strong> Found {self.report_data['duplicates']['exact_duplicates']:,} exact duplicates. Use <code>df.drop_duplicates()</code> to remove them.</li>"
            )
        
        # Outlier recommendations
        if self.report_data['outliers']['details']:
            impossible_cols = [d['column'] for d in self.report_data['outliers']['details'] if d['impossible_values']]
            if impossible_cols:
                recommendations.append(
                    f"<li><strong>Investigate Impossible Values:</strong> Columns {', '.join(impossible_cols[:3])} contain suspicious values that may be data entry errors.</li>"
                )
            
            high_outlier = [d for d in self.report_data['outliers']['details'] if d['outlier_pct'] > 10]
            if high_outlier:
                recommendations.append(
                    "<li><strong>Outlier Treatment:</strong> Consider capping, transforming (log), or removing outliers in high-impact columns.</li>"
                )
        
        # Type recommendations
        if self.report_data.get('data_types', {}).get('warnings'):
            recommendations.append(
                "<li><strong>Fix Data Types:</strong> Some columns may have incorrect types. Review and convert to appropriate types for better analysis.</li>"
            )
        
        if not recommendations:
            recommendations.append("<li>✅ Data quality looks good! Proceed with your analysis.</li>")

        return '\n'.join(recommendations)

    def _generate_categorical_html(self) -> str:
        """Generate HTML for categorical values analysis."""
        categorical_data = self.report_data.get('categorical', {})
        details = categorical_data.get('details', [])

        if not details:
            return "<p>No categorical columns found in the dataset.</p>"

        html_parts = []

        for col_info in details:
            col_name = col_info['column']
            unique_values = col_info['unique_values']
            value_counts = col_info['value_counts']
            unique_count = col_info['unique_count']

            # Create a collapsible section for each column (limit to 20 values)
            values_html = ""
            display_values = unique_values[:20]
            remaining_count = len(unique_values) - 20 if len(unique_values) > 20 else 0

            for val in display_values:
                count = value_counts.get(val, 0)
                pct = (count / len(self.df)) * 100
                # Handle NaN display
                display_val = str(val) if val is not None else "(null)"
                values_html += f"""
                <tr>
                    <td>{display_val}</td>
                    <td>{count:,}</td>
                    <td>{pct:.1f}%</td>
                </tr>
                """

            # Add row showing remaining values if truncated
            if remaining_count > 0:
                values_html += f"""
                <tr style="background: #f0f0f0; font-style: italic;">
                    <td colspan="3">... and {remaining_count:,} more values</td>
                </tr>
                """

            # Add null count if present
            null_count = self.df[col_name].isnull().sum()
            if null_count > 0:
                null_pct = (null_count / len(self.df)) * 100
                values_html += f"""
                <tr style="background: #fff3e0;">
                    <td><em>(missing/null)</em></td>
                    <td>{null_count:,}</td>
                    <td>{null_pct:.1f}%</td>
                </tr>
                """

            html_parts.append(f"""
            <div class="summary-section" style="margin-bottom: 15px;">
                <h4>{col_name} <span class="badge badge-success">{unique_count} unique values</span></h4>
                <table>
                    <thead>
                        <tr>
                            <th>Value</th>
                            <th>Count</th>
                            <th>Percentage</th>
                        </tr>
                    </thead>
                    <tbody>
                        {values_html}
                    </tbody>
                </table>
            </div>
            """)

        return '\n'.join(html_parts)

    def run_full_analysis(self, output_path: str = None) -> dict:
        """Run the complete data quality analysis pipeline."""
        print("\n" + "=" * 60)
        print("   DATA QUALITY REPORT")
        print("=" * 60)
        print(f"   File: {self.filepath.name}")
        print(f"   Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 60)
        
        if not self.load_data():
            return None
        
        self.analyze_missing_values()
        self.analyze_outliers()
        self.analyze_duplicates()
        self.analyze_data_types()
        self.analyze_categorical_values()

        # Generate HTML report
        report_path = self.generate_html_report(output_path)
        
        print("\n" + "=" * 60)
        print("   ANALYSIS COMPLETE")
        print("=" * 60)
        
        return self.report_data


def main():
    """Main entry point for command-line usage."""
    if len(sys.argv) < 2:
        print("Usage: python data_quality_report.py <path_to_csv>")
        print("\nExample: python data_quality_report.py data.csv")
        sys.exit(1)
    
    filepath = sys.argv[1]
    
    # Optional output path
    output_path = sys.argv[2] if len(sys.argv) > 2 else None
    
    # Run analysis
    report = DataQualityReport(filepath)
    report.run_full_analysis(output_path)


if __name__ == "__main__":
    main()
