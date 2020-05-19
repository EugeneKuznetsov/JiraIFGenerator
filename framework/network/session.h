#pragma once

#include <QObject>
#include <QUrl>
#include <QMap>

class QNetworkAccessManager;
class Reply;

class Session : public QObject
{
    Q_OBJECT
    Q_DISABLE_COPY(Session)

public:
    Session(const QUrl &server, QNetworkAccessManager *network, QObject *parent);

    Reply *get(const QUrl &uri, const QMap<QByteArray, QByteArray> &headers);
    Reply *post(const QUrl &uri, const QByteArray &payload, const QMap<QByteArray, QByteArray> &headers);

signals:
    void networkError(const QString &errorText);

private:
    QUrl completeUri(const QUrl &uri) const;

private:
    QNetworkAccessManager *m_network;
    QUrl                  m_server;
};
