{% macro setup_minio() %} 

  {% set setup_query %}
    INSTALL httpfs;
    LOAD httpfs;

    SET s3_endpoint='{{ env_var("MINIO_ENDPOINT") }}';
    SET s3_access_key_id='{{ env_var("MINIO_ACCESS_KEY") }}';
    SET s3_secret_access_key='{{ env_var("MINIO_SECRET_KEY") }}';
    SET s3_use_ssl=false;
    SET s3_url_style='path';
  {% endset %}

  {% do run_query(setup_query) %}

{% endmacro %}