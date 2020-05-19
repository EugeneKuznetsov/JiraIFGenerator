#include <QJsonDocument>
#include <QJsonObject>
#include <QVariant>
#include "responsestatus.h"

ResponseStatus::ResponseStatus(const qint32 statusCode, const QByteArray &data, const QMap<int, bool> &statuses)
    : QObject(nullptr)
    , m_statusCode(statusCode)
{
    QMap<int, bool>::const_iterator status = statuses.constFind(statusCode);
    m_success = (statuses.constEnd() == status) ? false : status.value();

    // parse only known errors
    if (!m_success && statuses.constEnd() != status) {
        QJsonDocument json = QJsonDocument::fromJson(data);
        QJsonObject root = json.object();
        m_errors = root["errorMessages"].toVariant().toStringList();
    }
}

bool ResponseStatus::getSuccess() const
{
    return m_success;
}

int ResponseStatus::getStatusCode() const
{
    return m_statusCode;
}

const QStringList &ResponseStatus::getErrors() const
{
    return m_errors;
}
