from flask import Flask, render_template
import yfinance as yf
import matplotlib
# Set the backend to 'Agg' before importing pyplot
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import io
import base64

app = Flask(__name__)

@app.route('/')
def index():
    # Expanded list of stocks to display
    stocks = [
        'ZYDUSLIFE.NS',
        'ZOMATO.NS','VHL.NS','UNIONBANK.NS',
        'UBL.NS','TITAGARH.NS',
        'TIINDIA.NS','SUZLON.NS','SIEMENS.NS','SCHAEFFLER.NS','SAFARI.NS','RECLTD.NS',
        'RADICO.NS','RAILTEL.NS','PFIZER.NS','PEL.NS','ONGC.NS',
        'NTPC.NS','NATIONALUM.NS',
        'MUTHOOTFIN.NS','MARUTI.NS','MRPL.NS',
        'MGL.NS','LATENTVIEW.NS','KOTAKBANK.NS',
        'KNRCON.NS','KICL.NS',
        'KPITTECH.NS',
        'KEI.NS','KCP.NS','JWL.NS','JSWSTEEL.NS','JSWHL.NS','JKTYRE.NS','JKPAPER.NS',
        'IREDA.NS','INDHOTEL.NS','IDFCFIRSTB.NS','ICICIPRULI.NS','HONDAPOWER.NS',
        'HEROMOTOCO.NS','HAVELLS.NS',
        'HDFCLIFE.NS','HDFCAMC.NS',
        'GREAVESCOT.NS','GAIL.NS','FSL.NS','ELGIEQUIP.NS','DIXON.NS','DATAPATTNS.NS','CUMMINSIND.NS',
        'CHOLAFIN.NS','CHENNPETRO.NS','CRISIL.NS','BHARATFORG.NS','BDL.NS','BERGEPAINT.NS',
        'DMART.NS','APARINDS.NS','ANDHRAPAP.NS','ACL.NS',

        'WIPRO.NS', 'VEDL.NS', 'SUNPHARMA.NS', 'SULA.NS', 'SAIL.NS', 
        'SOUTHBANK.NS', 'MOTHERSON.NS', 'SRF.NS', 'RAYMOND.NS', 'RAMCOSYS.NS', 
        'RAJESHEXPO.NS', 'PFC.NS', 'POLYCAB.NS', 'PERSISTENT.NS', 'POWERGRID.NS', 
        'OIL.NS', 'NMDC.NS', 'M&M.NS', 'MAHSEAMLES.NS', 'KTKBANK.NS', 
        'KALYANKJIL.NS', 'J&KBANK.NS', 'IRCTC.NS', 'HINDZINC.NS', 'GSPL.NS', 
        'GSFC.NS', 'GNFC.NS', 'GMDCLTD.NS', 'GESHIP.NS', 'FORCEMOT.NS', 
        'ESCORTS.NS', 'EICHERMOT.NS', 'DEEPAKFERT.NS', 'COALINDIA.NS', 
        'CUB.NS', 'CHOLAFIN.NS', 'CDSL.NS', 'CANBK.NS', 'CEATLTD.NS', 
        'CCL.NS', 'BHARTIARTL.NS', 'BPCL.NS', 'BALKRISIND.NS', 
        'BAJAJHLDNG.NS', 'BAJAJHFL.NS', 'BAJAJFINSV.NS', 'BAJFINANCE.NS', 
        'BAJAJ-AUTO.NS', 'APLAPOLLO.NS', 'VBL.NS', 'UBL.NS', 'UNITDSPR.NS', 
        'ULTRACEMCO.NS', 'TRENT.NS', 'TITAN.NS', 'THANGAMAYL.NS','TMB.NS', 'TECHM.NS', 
        'TATASTEEL.NS', 'TATAPOWER.NS', 'TATAMOTORS.NS', 'TATAINVEST.NS', 
        'TATACOMM.NS', 'TATACHEM.NS', 'TATAMOTORS.NS', 'TATAELXSI.NS', 
        'TATACONSUM.NS', 'RELIANCE.NS', 'PGHH.NS', 'PIDILITIND.NS', 
        'NESTLEIND.NS', 'MARICO.NS', 'MANAPPURAM.NS', 'IRFC.NS', 
        'INFY.NS', 'ITC.NS', 'ICICIBANK.NS', 'HINDUNILVR.NS', 
        'HINDALCO.NS', 'HDFCBANK.NS', 'HCLTECH.NS', 'EXIDEIND.NS', 
        'DRREDDY.NS', 'DIVISLAB.NS','DEEPAKFERT.NS', 'DEEPAKNTR.NS', 'COLPAL.NS', 
        'BRITANNIA.NS', 'ASIANPAINT.NS','APOLLOHOSP.NS', 'APOLLOTYRE.NS', 'ACC.NS', 
        'AMBUJACEM.NS','ITC.NS'
    ]

    
    stock_data = {}


    for stock in stocks:
        ticker = yf.Ticker(stock)
        stock_info = ticker.info

        try:
            stock_data[stock] = {
                'Current Price': stock_info['currentPrice'],
                '52 Week Low': stock_info['fiftyTwoWeekLow'],
                '52 Week High': stock_info['fiftyTwoWeekHigh']
            }
        except KeyError:
            print(f"Data not available for {stock}")
            continue

    # Sort stocks alphabetically in ascending order
    stock_names = stocks
    current_price = [stock_data[stock]['Current Price'] for stock in stock_names]
    low_52w = [stock_data[stock]['52 Week Low'] for stock in stock_names]
    high_52w = [stock_data[stock]['52 Week High'] for stock in stock_names]

    # Define the fixed width for the bars (all bars will be of the same width)
    bar_width = 90  # A constant width for all bars
    bar_start = 2500  # Move the bars to the center of the page

    # Create a clean horizontal bar plot with increased size
    fig, ax = plt.subplots(figsize=(8, 110))  # Increased width for better visibility

    y = np.arange(len(stock_names))

    # Loop through each stock to create bars and labels
    for i in range(len(stock_names)):
        bar_end = bar_start + bar_width  # All bars will end at the same fixed point

        # Plot a static bar of fixed length
        ax.plot([bar_start, bar_end], [i, i], color='lightblue', lw=5, zorder=1)

        # Calculate the relative position of the current price between the 52-week low and high
        if high_52w[i] > low_52w[i]:
            price_position = bar_start + (current_price[i] - low_52w[i]) / (high_52w[i] - low_52w[i]) * bar_width
        else:
            price_position = bar_start  # Edge case: if 52-week low equals high (or zero), place at start

        # Place a green arrow (↑) for the current price on the bar
        ax.annotate('▲', xy=(price_position, i), fontsize=15, color='green', ha='center', va='center', fontweight='bold')

        # Display the current price above the bar
        ax.text(price_position, i + 0.20, f'₹{current_price[i]:.2f}', va='center', ha='center', color='black', fontweight='bold')

        # Add bold low and high labels below the bar (moved closer)
        ax.text(bar_start, i - 0.30, f'L ₹{low_52w[i]:.2f}', va='center', ha='right', fontsize=10, fontweight='bold', color='black')
        ax.text(bar_end, i - 0.30, f'H ₹{high_52w[i]:.2f}', va='center', ha='left', fontsize=10, fontweight='bold', color='black')

    # Remove all axis ticks, labels, and grids
    ax.set_yticks(y)
    ax.set_yticklabels(stock_names, fontweight='bold')
    ax.xaxis.set_visible(False)
    ax.yaxis.set_ticks_position('none')
    ax.spines['top'].set_visible(False)
    ax.spines['bottom'].set_visible(False)
    ax.spines['left'].set_visible(False)
    ax.spines['right'].set_visible(False)

    # Increase vertical spacing between bars
    for i in range(len(stock_names)):
        ax.text(0, i, '', fontsize=1)  # This line adds spacing; you can adjust it

    # Save the plot to a BytesIO object and encode it as base64 for HTML rendering
    buf = io.BytesIO()
    plt.savefig(buf, format='png', bbox_inches='tight', transparent=True)
    buf.seek(0)
    plot_url = base64.b64encode(buf.read()).decode('utf-8')
    plt.close()

    return render_template('index.html', plot_url=plot_url)

if __name__ == '__main__':
    app.run(debug=True)
