# src/__init__.py
# Kenya Smart Agriculture — Source Package

from src.utils import (
    COUNTIES, COUNTY_MAP,
    normalise_county, season_of_date,
    compute_spi, ipc_label,
    IPC_COLOURS, SEASON_COLOURS,
    section,
)

from src.data_cleaner import (
    clean_nasa, aggregate_nasa_monthly, aggregate_nasa_seasonal,
    clean_ipc, clean_knbs_cpi, clean_news,
    merge_master,
)

from src.models import (
    prepare_classification_data,
    train_baseline_classifier, train_xgboost_classifier,
    evaluate_classifier, plot_confusion_matrix,
    evaluate_regression, compare_models,
    save_model, load_model,
)
