"""
Flask API for Super Store Analytics Dashboard
Converts Streamlit dashboard to RESTful API endpoints
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
import os
import warnings
from datetime import datetime
import json

warnings.filterwarnings('ignore')

app = Flask(__name__)
CORS(app)  # Enable CORS for frontend access

# ===== CONFIGURATION =====
DEFAULT_DATA_PATH = r'C:\Users\user\Desktop\MyMasterPiece\SuperStore Sales DataSet.xlsx'
UPLOAD_FOLDER = r'C:\Users\user\Desktop\MyMasterPiece\uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


# ===== UTILITY FUNCTIONS =====
def load_data(file_path=None):
    """Load and validate data from file or default source"""
    try:
        if file_path is not None:
            # Determine file type and read accordingly
            file_extension = file_path.split('.')[-1].lower()
            if file_extension == 'csv':
                df = pd.read_csv(file_path)
            elif file_extension in ['xlsx', 'xls']:
                df = pd.read_excel(file_path)
            else:
                return None, f"Unsupported file format: .{file_extension}"
        else:
            if not os.path.exists(DEFAULT_DATA_PATH):
                return None, "Default dataset not found"
            df = pd.read_excel(DEFAULT_DATA_PATH)
        
        # Validate data
        if df.empty:
            return None, "Uploaded file is empty"
        
        # Convert date columns
        date_columns = df.select_dtypes(include=['object']).columns
        for col in date_columns:
            try:
                df[col] = pd.to_datetime(df[col], errors='ignore')
            except:
                pass
        
        return df, None
        
    except Exception as e:
        return None, str(e)


def validate_date_columns(df):
    """Validate that required date columns exist"""
    if 'Order Date' not in df.columns:
        return False, "Missing 'Order Date' column"
    return True, None


def apply_filters(df, start_date=None, end_date=None, regions=None, states=None, cities=None):
    """Apply date and location filters to dataframe"""
    filtered_df = df.copy()
    
    # Date range filtering
    if start_date or end_date:
        try:
            if start_date:
                start_date = pd.to_datetime(start_date)
                filtered_df = filtered_df[filtered_df['Order Date'] >= start_date]
            if end_date:
                end_date = pd.to_datetime(end_date)
                filtered_df = filtered_df[filtered_df['Order Date'] <= end_date]
        except Exception as e:
            return None, f"Date filtering error: {str(e)}"
    
    # Region filtering
    if regions and len(regions) > 0:
        filtered_df = filtered_df[filtered_df['Region'].isin(regions)]
    
    # State filtering
    if states and len(states) > 0:
        filtered_df = filtered_df[filtered_df['State'].isin(states)]
    
    # City filtering
    if cities and len(cities) > 0:
        filtered_df = filtered_df[filtered_df['City'].isin(cities)]
    
    if filtered_df.empty:
        return None, "No data found with applied filters"
    
    return filtered_df, None


# ===== API ENDPOINTS =====

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'running',
        'message': 'Super Store Analytics API is operational'
    }), 200


@app.route('/api/load-data', methods=['GET', 'POST'])
def load_dataset():
    """Load default or uploaded dataset"""
    try:
        if request.method == 'POST':
            if 'file' not in request.files:
                return jsonify({'error': 'No file provided'}), 400
            
            file = request.files['file']
            if file.filename == '':
                return jsonify({'error': 'No file selected'}), 400
            
            # Save uploaded file
            file_path = os.path.join(UPLOAD_FOLDER, file.filename)
            file.save(file_path)
            df, error = load_data(file_path)
        else:
            # Load default data
            df, error = load_data()
        
        if error:
            return jsonify({'error': error}), 400
        
        # Validate date columns
        is_valid, validation_error = validate_date_columns(df)
        if not is_valid:
            return jsonify({'error': validation_error}), 400
        
        return jsonify({
            'success': True,
            'rows': len(df),
            'columns': len(df.columns),
            'columns_list': df.columns.tolist(),
            'date_range': {
                'start': df['Order Date'].min().isoformat(),
                'end': df['Order Date'].max().isoformat()
            }
        }), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/filter-options', methods=['GET', 'POST'])
def get_filter_options():
    """Get available filter options (regions, states, cities)"""
    try:
        df, error = load_data()
        if error:
            return jsonify({'error': error}), 400
        
        return jsonify({
            'regions': df['Region'].unique().tolist(),
            'states': df['State'].unique().tolist(),
            'cities': df['City'].unique().tolist(),
            'categories': df['Category'].unique().tolist() if 'Category' in df.columns else []
        }), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/kpis', methods=['POST'])
def get_kpis():
    """Calculate KPI metrics"""
    try:
        data = request.get_json()
        
        # Load and filter data
        df, error = load_data()
        if error:
            return jsonify({'error': error}), 400
        
        filtered_df, filter_error = apply_filters(
            df,
            start_date=data.get('start_date'),
            end_date=data.get('end_date'),
            regions=data.get('regions'),
            states=data.get('states'),
            cities=data.get('cities')
        )
        
        if filter_error:
            return jsonify({'error': filter_error}), 400
        
        # Calculate KPIs
        if 'Quantity' not in filtered_df.columns or 'Sales' not in filtered_df.columns:
            return jsonify({'error': 'Missing Quantity or Sales columns'}), 400
        
        filtered_df['Total_Sales'] = filtered_df['Sales'] * filtered_df['Quantity']
        
        total_qty = float(filtered_df['Quantity'].sum())
        total_sales = float(filtered_df['Total_Sales'].sum())
        total_categories = int(filtered_df['Category'].nunique())
        total_regions = int(filtered_df['Region'].nunique())
        avg_order_value = float(total_sales / max(len(filtered_df), 1))
        
        return jsonify({
            'total_transactions': total_qty,
            'total_sales': total_sales,
            'total_categories': total_categories,
            'total_regions': total_regions,
            'avg_order_value': avg_order_value,
            'records_count': len(filtered_df)
        }), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/category-sales', methods=['POST'])
def get_category_sales():
    """Get category-wise sales data"""
    try:
        data = request.get_json()
        
        df, error = load_data()
        if error:
            return jsonify({'error': error}), 400
        
        filtered_df, filter_error = apply_filters(
            df,
            start_date=data.get('start_date'),
            end_date=data.get('end_date'),
            regions=data.get('regions'),
            states=data.get('states'),
            cities=data.get('cities')
        )
        
        if filter_error:
            return jsonify({'error': filter_error}), 400
        
        category_df = filtered_df.groupby('Category', as_index=False)['Sales'].sum().sort_values('Sales', ascending=False)
        
        return jsonify({
            'categories': category_df['Category'].tolist(),
            'sales': category_df['Sales'].astype(float).tolist(),
            'data': category_df.to_dict('records')
        }), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/regional-sales', methods=['POST'])
def get_regional_sales():
    """Get regional sales distribution"""
    try:
        data = request.get_json()
        
        df, error = load_data()
        if error:
            return jsonify({'error': error}), 400
        
        filtered_df, filter_error = apply_filters(
            df,
            start_date=data.get('start_date'),
            end_date=data.get('end_date'),
            regions=data.get('regions'),
            states=data.get('states'),
            cities=data.get('cities')
        )
        
        if filter_error:
            return jsonify({'error': filter_error}), 400
        
        region_sales = filtered_df.groupby('Region', as_index=False)['Sales'].sum().sort_values('Sales', ascending=False)
        
        total_sales = region_sales['Sales'].sum()
        region_sales['percentage'] = (region_sales['Sales'] / total_sales * 100).round(2)
        
        return jsonify({
            'regions': region_sales['Region'].tolist(),
            'sales': region_sales['Sales'].astype(float).tolist(),
            'percentages': region_sales['percentage'].tolist(),
            'data': region_sales.to_dict('records')
        }), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/sales-funnel', methods=['POST'])
def get_sales_funnel():
    """Get sales funnel by region"""
    try:
        data = request.get_json()
        
        df, error = load_data()
        if error:
            return jsonify({'error': error}), 400
        
        filtered_df, filter_error = apply_filters(
            df,
            start_date=data.get('start_date'),
            end_date=data.get('end_date'),
            regions=data.get('regions'),
            states=data.get('states'),
            cities=data.get('cities')
        )
        
        if filter_error:
            return jsonify({'error': filter_error}), 400
        
        # Calculate Total_Sales if not present
        if 'Total_Sales' not in filtered_df.columns:
            filtered_df['Total_Sales'] = filtered_df['Sales'] * filtered_df['Quantity']
        
        funnel_stages = ['East', 'West', 'Central', 'South']
        funnel_values = []
        
        for stage in funnel_stages:
            value = filtered_df.loc[filtered_df['Region'] == stage, ['Total_Sales']]['Total_Sales'].sum()
            funnel_values.append(float(value))
        
        # Sort by values descending
        sorted_pairs = sorted(zip(funnel_stages, funnel_values), key=lambda x: x[1], reverse=True)
        funnel_stages_sorted, funnel_values_sorted = zip(*sorted_pairs)
        
        return jsonify({
            'stages': list(funnel_stages_sorted),
            'values': list(funnel_values_sorted),
            'data': [{'stage': s, 'value': v} for s, v in zip(funnel_stages_sorted, funnel_values_sorted)]
        }), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/quantity-sales-correlation', methods=['POST'])
def get_quantity_sales_correlation():
    """Get scatter plot data for quantity vs sales"""
    try:
        data = request.get_json()
        
        df, error = load_data()
        if error:
            return jsonify({'error': error}), 400
        
        filtered_df, filter_error = apply_filters(
            df,
            start_date=data.get('start_date'),
            end_date=data.get('end_date'),
            regions=data.get('regions'),
            states=data.get('states'),
            cities=data.get('cities')
        )
        
        if filter_error:
            return jsonify({'error': filter_error}), 400
        
        # Limit to first 1000 points for performance
        plot_data = filtered_df[['Quantity', 'Sales']].head(1000)
        
        return jsonify({
            'quantities': plot_data['Quantity'].astype(int).tolist(),
            'sales': plot_data['Sales'].astype(float).tolist(),
            'data': plot_data.to_dict('records')
        }), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/correlation-matrix', methods=['POST'])
def get_correlation_matrix():
    """Get correlation matrix for numerical features"""
    try:
        data = request.get_json()
        
        df, error = load_data()
        if error:
            return jsonify({'error': error}), 400
        
        filtered_df, filter_error = apply_filters(
            df,
            start_date=data.get('start_date'),
            end_date=data.get('end_date'),
            regions=data.get('regions'),
            states=data.get('states'),
            cities=data.get('cities')
        )
        
        if filter_error:
            return jsonify({'error': filter_error}), 400
        
        numeric_df = filtered_df.select_dtypes(include=['number']).copy()
        
        if numeric_df.shape[1] == 0:
            return jsonify({'error': 'No numerical data available'}), 400
        
        correlation_matrix = numeric_df.corr(method='pearson')
        
        return jsonify({
            'columns': correlation_matrix.columns.tolist(),
            'correlation_matrix': correlation_matrix.values.tolist(),
            'matrix_dict': correlation_matrix.to_dict()
        }), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/summary-statistics', methods=['POST'])
def get_summary_statistics():
    """Get summary statistics for filtered data"""
    try:
        data = request.get_json()
        
        df, error = load_data()
        if error:
            return jsonify({'error': error}), 400
        
        filtered_df, filter_error = apply_filters(
            df,
            start_date=data.get('start_date'),
            end_date=data.get('end_date'),
            regions=data.get('regions'),
            states=data.get('states'),
            cities=data.get('cities')
        )
        
        if filter_error:
            return jsonify({'error': filter_error}), 400
        
        numeric_cols = filtered_df.select_dtypes(include=['number']).columns.tolist()
        
        if not numeric_cols:
            return jsonify({'error': 'No numerical columns available'}), 400
        
        summary_stats = filtered_df[numeric_cols].describe().round(2)
        
        return jsonify({
            'statistics': summary_stats.to_dict(),
            'summary': {
                'count': summary_stats.loc['count'].to_dict(),
                'mean': summary_stats.loc['mean'].to_dict(),
                'std': summary_stats.loc['std'].to_dict(),
                'min': summary_stats.loc['min'].to_dict(),
                'max': summary_stats.loc['max'].to_dict()
            }
        }), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/dataset-overview', methods=['POST'])
def get_dataset_overview():
    """Get dataset overview and metadata"""
    try:
        data = request.get_json()
        
        df, error = load_data()
        if error:
            return jsonify({'error': error}), 400
        
        filtered_df, filter_error = apply_filters(
            df,
            start_date=data.get('start_date'),
            end_date=data.get('end_date'),
            regions=data.get('regions'),
            states=data.get('states'),
            cities=data.get('cities')
        )
        
        if filter_error:
            return jsonify({'error': filter_error}), 400
        
        return jsonify({
            'total_records': len(filtered_df),
            'total_columns': len(filtered_df.columns),
            'missing_values': int(filtered_df.isna().sum().sum()),
            'columns': filtered_df.columns.tolist(),
            'data_types': filtered_df.dtypes.astype(str).to_dict()
        }), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/raw-data', methods=['POST'])
def get_raw_data():
    """Get raw data (paginated)"""
    try:
        data = request.get_json()
        page = data.get('page', 1)
        limit = data.get('limit', 100)
        columns = data.get('columns', None)
        
        df, error = load_data()
        if error:
            return jsonify({'error': error}), 400
        
        filtered_df, filter_error = apply_filters(
            df,
            start_date=data.get('start_date'),
            end_date=data.get('end_date'),
            regions=data.get('regions'),
            states=data.get('states'),
            cities=data.get('cities')
        )
        
        if filter_error:
            return jsonify({'error': filter_error}), 400
        
        # Pagination
        start = (page - 1) * limit
        end = start + limit
        
        if columns:
            filtered_df = filtered_df[columns]
        
        paginated_data = filtered_df.iloc[start:end]
        
        # Convert dates to ISO format
        for col in paginated_data.columns:
            if pd.api.types.is_datetime64_any_dtype(paginated_data[col]):
                paginated_data[col] = paginated_data[col].astype(str)
        
        return jsonify({
            'data': paginated_data.to_dict('records'),
            'page': page,
            'limit': limit,
            'total_records': len(filtered_df),
            'total_pages': (len(filtered_df) + limit - 1) // limit
        }), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/export-data', methods=['POST'])
def export_data():
    """Export filtered data as CSV"""
    try:
        from flask import send_file
        import io
        
        data = request.get_json()
        
        df, error = load_data()
        if error:
            return jsonify({'error': error}), 400
        
        filtered_df, filter_error = apply_filters(
            df,
            start_date=data.get('start_date'),
            end_date=data.get('end_date'),
            regions=data.get('regions'),
            states=data.get('states'),
            cities=data.get('cities')
        )
        
        if filter_error:
            return jsonify({'error': filter_error}), 400
        
        # Create CSV in memory
        csv_buffer = io.StringIO()
        filtered_df.to_csv(csv_buffer, index=False)
        csv_buffer.seek(0)
        
        return jsonify({
            'success': True,
            'csv': csv_buffer.getvalue(),
            'rows': len(filtered_df)
        }), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# ===== ERROR HANDLERS =====
@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Endpoint not found'}), 404


@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Internal server error'}), 500


# ===== MAIN =====
if __name__ == '__main__':
    app.run(
        debug=True,
        host='0.0.0.0',
        port=5000,
        threaded=True
    )
