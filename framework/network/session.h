#pragma once

#include <QObject>
#include <QNetworkRequest>
#include <QSslConfiguration>
#include <QUrl>
#include <QMap>

class QNetworkAccessManager;
class QNetworkRequest;
class Reply;

class Session : public QObject
{
    Q_OBJECT
    Q_DISABLE_COPY(Session)

public:
    Session(const QUrl &server, QNetworkAccessManager *network, QObject *parent);

    const QUrl &getServer() const;

    Reply *get(const QUrl &uri, const QMap<QByteArray, QByteArray> &headers);
    Reply *post(const QUrl &uri, const QByteArray &payload, const QMap<QByteArray, QByteArray> &headers);
    Reply *put(const QUrl &uri, const QByteArray &payload, const QMap<QByteArray, QByteArray> &headers);
    Reply *deleteResource(const QUrl &uri, const QMap<QByteArray, QByteArray> &headers);

signals:
    void networkError(const QString &errorText);

public slots:
    void setupCaCertificateFile(const QString &certificateFile);

private:
    QUrl completeUri(const QUrl &uri) const;
    QNetworkRequest createRequest(const QUrl &uri, const QMap<QByteArray, QByteArray> &headers) const;

private:
    QNetworkAccessManager *m_network;
    QUrl                  m_server;
    QSslConfiguration     m_sslConfiguration;
};
