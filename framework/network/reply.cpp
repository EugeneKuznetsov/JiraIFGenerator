#include <QNetworkReply>
#include "reply.h"

Reply::Reply(QNetworkReply *networkReply, QObject *parent)
    : QObject(parent)
    , m_networkReply(networkReply)
{
    if (nullptr != networkReply)
        networkReply->setParent(this);

    // https://wiki.qt.io/New_Signal_Slot_Syntax#Overload
    void (QNetworkReply:: *errorSignal)(QNetworkReply::NetworkError) = &QNetworkReply::error;
    connect(networkReply, errorSignal, this, [this, networkReply](QNetworkReply::NetworkError) {
        // we are interested only in network layer and proxy errors
        // as of Qt 5.14, they are defined before ContentAccessDenied literal
        if (networkReply->error() < QNetworkReply::ContentAccessDenied)
            emit networkError(m_networkReply->errorString());
    });
    connect(networkReply, &QNetworkReply::finished, this, &Reply::onReady);
}

void Reply::onReady()
{
    const qint32 statusCode = m_networkReply->attribute(QNetworkRequest::HttpStatusCodeAttribute).toInt();
    const QByteArray data = m_networkReply->readAll();

    if (0 != statusCode)
        emit ready(statusCode, data);

    emit destroy();
}
