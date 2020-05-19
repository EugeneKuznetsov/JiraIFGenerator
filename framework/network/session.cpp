#include <QNetworkAccessManager>
#include <QNetworkRequest>
#include <QNetworkReply>
#include "reply.h"
#include "session.h"

Session::Session(const QUrl &server, QNetworkAccessManager *network, QObject *parent)
    : QObject(parent)
    , m_network(network)
    , m_server(server)
{
}

Reply *Session::get(const QUrl &uri, const QMap<QByteArray, QByteArray> &headers)
{
    if (nullptr == m_network)
        return nullptr;

    QNetworkRequest request(completeUri(uri));
    for (auto header : headers.toStdMap())
       request.setRawHeader(header.first, header.second);

    return new Reply(m_network->get(request), this);
}

Reply *Session::post(const QUrl &uri, const QByteArray &payload, const QMap<QByteArray, QByteArray> &headers)
{
    if (nullptr == m_network)
        return nullptr;

    QNetworkRequest request(completeUri(uri));
    for (auto header : headers.toStdMap())
       request.setRawHeader(header.first, header.second);

    return new Reply(m_network->post(request, payload), this);
}

QUrl Session::completeUri(const QUrl &uri) const
{
    return QUrl(m_server.toString() + uri.toString());
}
