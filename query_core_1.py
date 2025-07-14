def query_core_1(user_query):
    user_query = user_query.lower()

    # Core_1 Simulated Knowledge: Anaplan + Supply Chain
    core_knowledge = {
        # 🔁 Anaplan Model Building
        "sum and lookup": (
            "Use SUM to aggregate based on a list-formatted line item. Combine with LOOKUP to map across dimensions.\n"
            "Example: 'Volumes Received'[SUM: SYS Mapping.Store, LOOKUP: SYS Mapping.Week]"
        ),
        "offset": (
            "OFFSET shifts data by N time periods. Use it with SYS Parameters for lead time modeling.\n"
            "Example: OFFSET(Demand, SYS Parameters.Lead Time, 0)"
        ),
        "movingsum" : (
            "MOVINGSUM is used for rolling averages like a 5-week demand window.\n"
            "Example: MOVINGSUM(Final Demand, 0, 4) / 5"
        ),
        "timesum": (
            "TIMESUM aggregates values across time.\n"
            "Example: TIMESUM(Forecast, START(), END()) for a custom range total."
        ),
        "weeks of supply" : (
            "WoS = Ending Inventory / (MOVINGSUM(Final Demand, 0, 4) / 5).\n"
            "Use SYS Time flags to reset quarterly averages cleanly."
        ),
        "lead time" : (
            "Lead time logic: OFFSET(Demand, SYS SKU.Lead Time, 0).\n"
            "Ensure Lead Time is dynamic at SKU or location level."
        ),
        "baseline" : (
            "Baselines are saved references of past plans (Budget, LY). Snapshot into separate line items for comparisons."
        ),
        "constraint supply" : (
            "Constrained Supply logic allocates limited stock by demand priority.\n"
            "Stage 1: Reserve for committed. Stage 2: Allocate by priority %.\n"
            "Use MAX caps, flags, and persistent override options."
        ),
        "snapshot" : (
            "Snapshots capture plan data at a point in time. Use a flag like 'Snap Trigger' and a process to copy line items."
        ),
        "scenario planning" : (
            "Use Numbered Lists to create scenario variations. Control drivers via SELECTED Scenario modules."
        ),
        "circular reference": (
            "To avoid circular references in Anaplan, isolate calculations using system modules or split formulas over stages."
        ),
        "timescale mismatch": (
            "Ensure line item time scale aligns with model logic: consider override at line-item level when necessary."
        ),
        "resetting wos": (
            "Reset your WoS calculation quarterly by checking SYS Time.IsQuarterStart and using IF THEN logic to restart averages."
        ),

        # 📦 Supply Chain Knowledge
        "supply chain planning": (
            "A robust supply chain plan includes:\n"
            "- Demand Forecasting\n"
            "- Supply & Capacity Planning\n"
            "- Inventory Optimization\n"
            "- Constraint-based allocation\n"
            "Reference: Simchi-Levi’s Hierarchical Planning Framework."
        ),
        "demand planning": (
            "Demand planning balances historical forecasts with seasonality, promotions, and causal factors.\n"
            "Use MOVINGSUM, overrides, and forecast bias tracking."
        ),
        "inventory optimization": (
            "Use MIN/MAX policy, reorder points, and safety stock buffers.\n"
            "Lead time variability is a key driver — consider stochastic models for high-variance items."
        ),
        "bullwhip effect": (
            "Bullwhip effect describes demand amplification in the supply chain.\n"
            "Reduce it by:\n"
            "- Sharing upstream demand\n"
            "- Reducing lead times\n"
            "- Smoothing orders and batch sizes"
        ),
        "scm kpis": (
            "Key KPIs in SCM:\n"
            "- Fill Rate\n"
            "- OTIF (On Time In Full)\n"
            "- Inventory Turns\n"
            "- Supply Plan Adherence"
        ),
        "network design": (
            "Supply Chain Network Design includes facility location, flow paths, and cost-to-serve modeling.\n"
            "Use scenario planning to evaluate fixed + variable trade-offs."
        ),
        "transportation planning": (
            "Optimize transport using route-based cost models, carrier performance data, and load consolidation strategies."
        ),
        "capacity planning": (
            "Balance machine, labor, and vendor capacity with forecasted demand.\n"
            "Plan at monthly buckets, and firm at weekly/daily in operational windows."
        ),
        "mrp" : (
            "Material Requirements Planning (MRP) explodes demand from FG → components.\n"
            "Use lead times, batch sizes, and BOM logic to determine net requirements."
        )
    }

    # Keyword Search (Partial Match)
    for keyword, response in core_knowledge.items():
        if keyword in user_query:
            return response

    return ""  # Let fallback handle if no match
