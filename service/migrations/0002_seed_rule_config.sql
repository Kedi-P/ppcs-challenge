-- 0002_seed_rule_config.sql — baseline PPCS rule thresholds
--
-- Was/Now compliance rules the app enforces. Seeded so a freshly-branched
-- clone (or a new team schema) has working config out of the box.

INSERT INTO :schema.ppcs_rule_config (rule_id, param_key, param_value)
VALUES
    ('PPCS-055', 'min_discount_pct',  5),
    ('PPCS-055', 'min_duration_days', 7)
ON CONFLICT (rule_id, param_key) DO UPDATE
    SET param_value = EXCLUDED.param_value,
        updated_at  = now();
