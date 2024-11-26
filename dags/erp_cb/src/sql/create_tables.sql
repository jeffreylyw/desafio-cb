CREATE TABLE IF NOT EXISTS guest_checks (
    guestCheckId BIGINT PRIMARY KEY,
    chkNum INT,
    opnBusDt DATE,
    opnUTC TIMESTAMP,
    clsdBusDt DATE,
    clsdUTC TIMESTAMP,
    subTtl NUMERIC,
    nonTxblSlsTtl NUMERIC,
    chkTtl NUMERIC,
    dscTtl NUMERIC,
    payTtl NUMERIC,
    balDueTtl NUMERIC,
    rvcNum INT,
    otNum INT,
    ocNum INT,
    tblNum INT,
    tblName TEXT,
    empNum BIGINT,
    numSrvcRd INT,
    numChkPrntd INT,
    lastTransUTC TIMESTAMP,
    lastTransLcl TIMESTAMP,
    lastUpdatedUTC TIMESTAMP,
    lastUpdatedLcl TIMESTAMP,
    clsdFlag BOOLEAN,
    gstCnt INT
);

CREATE TABLE IF NOT EXISTS taxes (
    taxId SERIAL PRIMARY KEY,
    guestCheckId BIGINT REFERENCES guest_checks(guestCheckId),
    taxNum INT,
    txblSlsTtl NUMERIC,
    taxCollTtl NUMERIC,
    taxRate NUMERIC,
    type INT
);

CREATE TABLE IF NOT EXISTS detail_lines (
    guestCheckLineItemId BIGINT PRIMARY KEY,
    guestCheckId BIGINT REFERENCES guest_checks(guestCheckId),
    rvcNum INT,
    dtlOtNum INT,
    dtlOcNum INT,
    lineNum INT,
    dtlId INT,
    detailUTC TIMESTAMP,
    detailLcl TIMESTAMP,
    lastUpdateUTC TIMESTAMP,
    lastUpdateLcl TIMESTAMP,
    busDt DATE,
    wsNum INT,
    dspTtl NUMERIC,
    dspQty INT,
    aggTtl NUMERIC,
    aggQty INT,
    chkEmpId BIGINT,
    chkEmpNum BIGINT,
    svcRndNum INT,
    seatNum INT
);

CREATE TABLE IF NOT EXISTS menu_items (
    menuItemId SERIAL PRIMARY KEY,
    guestCheckLineItemId BIGINT REFERENCES detail_lines(guestCheckLineItemId),
    miNum INT,
    modFlag BOOLEAN,
    inclTax NUMERIC,
    activeTaxes TEXT,
    prcLvl INT
);
