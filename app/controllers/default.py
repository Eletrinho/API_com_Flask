from app import api, db, ns
from flask import jsonify, abort
from flask_restx import Resource, fields
from app.models.table import FilmesDB

filmes_model = api.model("Model",{
    'id': fields.Integer(readonly=True, description='Id do filme'),
    'name': fields.String(required=True, description='Nome do filme'),
    'year': fields.Integer(required=True, description='Ano em que foi lançado'),
    'profit': fields.Float(description='O quanto o filme faturou')
})

@ns.route('/')
class Filmes(Resource):

    def get(self):
        filmes_dict = []
        filmes_list = FilmesDB.query.all()
        for film in filmes_list:
            filmes_dict.append(film.get())
        return jsonify(filmes_dict)

    @ns.expect(filmes_model, validate=True)
    @ns.marshal_with(filmes_model)
    def post(self):
        new_movie = FilmesDB(name=api.payload.get("name"), year=api.payload.get("year"), profit=api.payload.get("profit"))
        db.session.add(new_movie)
        db.session.commit()
        return new_movie.get(), 201

@ns.route("/<int:id>")
@ns.response(404, "Filme não encontrado")
@ns.param('id', 'Id do filme')
class FilmesEdit(Resource):

    def get(self, id):
        filme = FilmesDB.query.get(id) or abort(404, f"Filme de Id {id}, não encontrado.")
        return jsonify(filme.get())

    @ns.doc('Deletar filme')
    @ns.response(204, 'Filme deletado')
    def delete(self, id):
        filme = FilmesDB.query.get(id) or abort(404, f"Filme de Id {id}, não encontrado.")
        db.session.delete(filme)
        db.session.commit()
        return jsonify({'filme_deletado': filme.get()})

    @ns.expect(filmes_model)
    @ns.marshal_with(filmes_model)
    def put(self, id):
        filme = FilmesDB.query.get(id) or abort(404, f"Filme de Id {id}, não encontrado.")
        filme.update(name=api.payload.get("name"), year=api.payload.get("year"), profit=api.payload.get("profit"))
        db.session.commit()
        return filme.get(), 201
        