class Page < ApplicationRecord
  validates :url,
    presence: true,
    uniqueness: true,
    url: true

  validates :parsed_data,
    presence: true

  enum file_type: {
    pdf: 'pdf',
    doc: 'doc',
    docx: 'docx',
    html: 'html',
  }, _suffix: true
end
