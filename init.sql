DROP TABLE IF EXISTS clickup.website_sprint;

CREATE TABLE clickup.website_sprint
(
    task_id         varchar,
    name            varchar,
    parent          varchar,
    status          varchar,
    creator         varchar,
    assignee        varchar,
    time_estimate   real,
    date_closed     timestamp,
    PRIMARY KEY (task_id)
);

CREATE INDEX IF NOT EXISTS clickup_website_sprint_date_closed ON clickup.website_sprint (date_closed);
